import os
from decimal import Decimal
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.models.product import Product
from app.models.imports import Import, ImportItem, CityStock
from app.models.sale import PaymentMethod
from app.schemas.imports import ImportCreate, ImportItemCreate, CityDistribution
from app.schemas.sale import SaleCreate
from app.usecases.import_metrics import ImportMetricsUseCase
from app.api.v1.endpoints.imports import create_import as api_create_import
from app.api.v1.endpoints.sales import create_sale as api_create_sale
from app.dashboard.deps import get_dashboard_user, COOKIE_NAME

router = APIRouter(prefix="/dashboard")

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


# ---------- Auth ----------

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password) or not user.is_staff:
        return templates.TemplateResponse(
            request, "login.html", {"error": "Credenciales inválidas"}, status_code=401
        )
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(COOKIE_NAME, create_access_token(str(user.id)), httponly=True)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse("/dashboard/login", status_code=303)
    response.delete_cookie(COOKIE_NAME)
    return response


# ---------- Lotes ----------

@router.get("", response_class=HTMLResponse)
async def imports_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_dashboard_user),
):
    result = await db.execute(
        select(Import).options(selectinload(Import.items)).order_by(Import.created_at.desc())
    )
    imports = result.scalars().all()
    uc = ImportMetricsUseCase(db)
    summaries = [await uc.summary(imp) for imp in imports]
    return templates.TemplateResponse(
        request, "imports_list.html", {"summaries": summaries, "user": user}
    )


@router.get("/imports/{import_id}", response_class=HTMLResponse)
async def import_detail(
    import_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_dashboard_user),
):
    metrics = await ImportMetricsUseCase(db).metrics(import_id)
    if not metrics:
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse(
        request, "import_detail.html", {"m": metrics, "user": user}
    )


# ---------- Formulario: nueva venta ----------

async def _sale_form_options(db: AsyncSession) -> list[dict]:
    """Opciones ítem+ciudad con stock disponible para el select del formulario."""
    result = await db.execute(
        select(CityStock, ImportItem, Import.name.label("import_name"), Product.name.label("product_name"))
        .join(ImportItem, CityStock.import_item_id == ImportItem.id)
        .join(Import, ImportItem.import_id == Import.id)
        .join(Product, ImportItem.product_id == Product.id)
        .where(CityStock.quantity > 0)
        .order_by(Import.created_at.desc(), Product.name)
    )
    return [
        {
            "value": f"{r.ImportItem.id}|{r.CityStock.city}",
            "label": f"{r.import_name} — {r.product_name} — {r.CityStock.city} (stock: {r.CityStock.quantity})",
        }
        for r in result.all()
    ]


@router.get("/sales/new", response_class=HTMLResponse)
async def sale_form(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_dashboard_user),
):
    options = await _sale_form_options(db)
    return templates.TemplateResponse(
        request, "sale_form.html",
        {"options": options, "payment_methods": [m.value for m in PaymentMethod], "user": user, "error": None, "ok": None},
    )


@router.post("/sales/new", response_class=HTMLResponse)
async def sale_submit(
    request: Request,
    item_city: str = Form(...),
    quantity: int = Form(...),
    unit_price: Decimal = Form(...),
    payment_method: str = Form("cash"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_dashboard_user),
):
    import_item_id, city = item_city.split("|", 1)
    error = ok = None
    try:
        payload = SaleCreate(
            import_item_id=int(import_item_id),
            city=city,
            quantity=quantity,
            unit_price=unit_price,
            payment_method=PaymentMethod(payment_method),
        )
        sale = await api_create_sale(payload, db=db, current_user=user)
        ok = f"Venta #{sale.id} registrada: {quantity} × {unit_price} Bs en {city}"
    except Exception as e:
        detail = getattr(e, "detail", None) or str(e)
        error = f"No se pudo registrar la venta: {detail}"

    options = await _sale_form_options(db)
    return templates.TemplateResponse(
        request, "sale_form.html",
        {"options": options, "payment_methods": [m.value for m in PaymentMethod], "user": user, "error": error, "ok": ok},
    )


# ---------- Formulario: nuevo lote ----------

@router.get("/imports/new/form", response_class=HTMLResponse)
async def import_form(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_dashboard_user),
):
    products = (await db.execute(select(Product).order_by(Product.name))).scalars().all()
    return templates.TemplateResponse(
        request, "import_form.html", {"products": products, "user": user, "error": None, "ok": None}
    )


def _parse_distribution(raw: str) -> list[CityDistribution]:
    """Parsea "Sucre:60, La Paz:40" a distribución por ciudades."""
    dist = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        city, _, qty = part.rpartition(":")
        dist.append(CityDistribution(city=city.strip(), quantity=int(qty.strip())))
    return dist


@router.post("/imports/new/form", response_class=HTMLResponse)
async def import_submit(
    request: Request,
    name: str = Form(...),
    shipping_cost: Decimal = Form(Decimal("0")),
    notes: str = Form(""),
    product_id: list[int] = Form(...),
    quantity: list[int] = Form(...),
    purchase_cost: list[Decimal] = Form(...),
    distribution: list[str] = Form(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_dashboard_user),
):
    error = ok = None
    try:
        items = [
            ImportItemCreate(
                product_id=pid,
                quantity=qty,
                purchase_cost=cost,
                distribution=_parse_distribution(dist),
            )
            for pid, qty, cost, dist in zip(product_id, quantity, purchase_cost, distribution)
        ]
        payload = ImportCreate(
            name=name, shipping_cost=shipping_cost, notes=notes or None, items=items
        )
        created = await api_create_import(payload, db=db, current_user=user)
        ok = f"Lote '{created.name}' creado con {len(created.items)} ítems"
    except Exception as e:
        detail = getattr(e, "detail", None) or str(e)
        error = f"No se pudo crear el lote: {detail}"

    products = (await db.execute(select(Product).order_by(Product.name))).scalars().all()
    return templates.TemplateResponse(
        request, "import_form.html", {"products": products, "user": user, "error": error, "ok": ok}
    )
