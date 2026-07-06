from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.core.deps import get_current_admin
from app.models.user import User
from app.models.product import Product
from app.models.imports import Import, ImportItem, CityStock
from app.models.sale import Sale
from app.schemas.imports import (
    ImportCreate, ImportUpdate, ImportRead, ImportItemRead, CityStockRead,
    ImportSummary, ImportMetrics,
)
from app.usecases.import_costs import compute_unit_cost
from app.usecases.import_metrics import ImportMetricsUseCase

router = APIRouter()


def _to_read(imp: Import) -> ImportRead:
    return ImportRead(
        id=imp.id,
        name=imp.name,
        shipping_cost=imp.shipping_cost,
        notes=imp.notes,
        created_at=imp.created_at,
        items=[
            ImportItemRead(
                id=i.id,
                product_id=i.product_id,
                product_name=i.product.name if i.product else None,
                quantity=i.quantity,
                purchase_cost=i.purchase_cost,
                unit_cost=i.unit_cost,
                city_stocks=[CityStockRead.model_validate(cs) for cs in i.city_stocks],
            )
            for i in imp.items
        ],
    )


async def _load_import(db: AsyncSession, import_id: int) -> Import | None:
    result = await db.execute(
        select(Import)
        .where(Import.id == import_id)
        .options(
            selectinload(Import.items).selectinload(ImportItem.city_stocks),
            selectinload(Import.items).selectinload(ImportItem.product),
        )
    )
    return result.scalar_one_or_none()


@router.post("/imports/", response_model=ImportRead, status_code=status.HTTP_201_CREATED)
async def create_import(
    payload: ImportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    product_ids = [item.product_id for item in payload.items]
    result = await db.execute(select(Product.id).where(Product.id.in_(product_ids)))
    found = {r for (r,) in result.all()}
    missing = set(product_ids) - found
    if missing:
        raise HTTPException(status_code=404, detail=f"Productos inexistentes: {sorted(missing)}")

    n_items = len(payload.items)
    imp = Import(
        name=payload.name,
        shipping_cost=payload.shipping_cost,
        notes=payload.notes,
        created_at=date.today(),
    )
    db.add(imp)
    await db.flush()

    for item in payload.items:
        db_item = ImportItem(
            import_id=imp.id,
            product_id=item.product_id,
            quantity=item.quantity,
            purchase_cost=item.purchase_cost,
            unit_cost=compute_unit_cost(
                item.purchase_cost, payload.shipping_cost, n_items, item.quantity
            ),
        )
        db.add(db_item)
        await db.flush()
        for dist in item.distribution:
            db.add(CityStock(import_item_id=db_item.id, city=dist.city, quantity=dist.quantity))

    await db.commit()
    return _to_read(await _load_import(db, imp.id))


@router.get("/imports/", response_model=list[ImportSummary])
async def list_imports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    result = await db.execute(
        select(Import).options(selectinload(Import.items)).order_by(Import.created_at.desc())
    )
    imports = result.scalars().all()
    uc = ImportMetricsUseCase(db)
    return [await uc.summary(imp) for imp in imports]


@router.get("/imports/{import_id}", response_model=ImportRead)
async def get_import(
    import_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    imp = await _load_import(db, import_id)
    if not imp:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return _to_read(imp)


@router.get("/imports/{import_id}/metrics", response_model=ImportMetrics)
async def import_metrics(
    import_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    metrics = await ImportMetricsUseCase(db).metrics(import_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return metrics


@router.patch("/imports/{import_id}", response_model=ImportRead)
async def update_import(
    import_id: int,
    payload: ImportUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    imp = await _load_import(db, import_id)
    if not imp:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    if payload.name is not None:
        imp.name = payload.name
    if payload.notes is not None:
        imp.notes = payload.notes
    if payload.shipping_cost is not None:
        imp.shipping_cost = payload.shipping_cost
        # El costo unitario queda fijo salvo edición explícita: recalcular todos los ítems
        n_items = len(imp.items)
        for item in imp.items:
            item.unit_cost = compute_unit_cost(
                item.purchase_cost, imp.shipping_cost, n_items, item.quantity
            )

    sales_count = (
        await db.execute(
            select(func.count(Sale.id))
            .join(ImportItem, Sale.import_item_id == ImportItem.id)
            .where(ImportItem.import_id == import_id)
        )
    ).scalar_one()

    await db.commit()
    response = _to_read(await _load_import(db, import_id))
    if sales_count:
        # Se informa vía header: las métricas siempre usan el unit_cost vigente
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content={**response.model_dump(mode="json"), "warning": f"{sales_count} ventas ya registradas en este lote; el costo unitario fue recalculado"},
        )
    return response
