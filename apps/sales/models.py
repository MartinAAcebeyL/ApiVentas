from django.db.models import F, Sum
from django.db import models


class Sale(models.Model):
    class Meta:
        db_table = "sales"
        verbose_name = "sale"
        verbose_name_plural = "sales"

    seller = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ManyToManyField("products.Product", related_name="sale_products")


class SaleDetail(models.Model):
    class Meta:
        db_table = "sales_details"
        verbose_name = "sale_detail"
        verbose_name_plural = "sales_details"

    PAYMENT_METHODS = (("cash", "Cash"), ("qr", "Qr"), ("transfer", "Transfer"))

    sale = models.OneToOneField("Sale", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    @classmethod
    def get_total_price_between_dates(cls, start_date: str, end_date: str) -> float:
        total = SaleDetail.objects.filter(
            created_at__range=(start_date, end_date)
        ).aggregate(Sum("total"))

        return total["total__sum"] or 0

    @classmethod
    def get_total_price_between_dates_and_category(
        cls, category: str, start_date: str, end_date: str
    ) -> float:
        total = SaleDetail.objects.filter(
            created_at__range=(start_date, end_date),
            sale__product__category__name=category,
        ).aggregate(Sum("total"))

        return total["total__sum"] or 0

    @classmethod
    def get_sale_details_between_dates_and_category(
        cls, category: str, start_date: str, end_date: str
    ) -> list:
        sale_detail = SaleDetail.objects.filter(
            created_at__range=(start_date, end_date),
            sale__product__category__name=category,
        ).values(
            "id",
            "sale",
            "quantity",
            "total",
            "unit_price",
            "created_at",
            name=F("sale__product__name"),
        )

        return list(sale_detail)


class Shipment(models.Model):
    class Meta:
        db_table = "shipments"
        verbose_name = "shipment"
        verbose_name_plural = "shipments"

    DEPARTAMENT_CHOICES = (
        ("La Paz", "La Paz"),
        ("Cochabamba", "Cochabamba"),
        ("Santa Cruz", "Santa Cruz"),
        ("Oruro", "Oruro"),
        ("Potosi", "Potosi"),
        ("Tarija", "Tarija"),
        ("Beni", "Beni"),
        ("Pando", "Pando"),
        ("Chuquisaca", "Chuquisaca"),
    )

    ESTATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_transit", "In transit"),
        ("delivered", "Delivered"),
    )

    sale = models.OneToOneField("Sale", on_delete=models.CASCADE)
    departament = models.CharField(max_length=12, choices=DEPARTAMENT_CHOICES)
    city = models.CharField(max_length=255, default="Sucre")
    shipment_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ESTATUS_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    @classmethod
    def get_shipment_cost_between_dates_and_category(
        cls, category: str, start_date: str, end_date: str
    ):
        shipment_cost = Shipment.objects.filter(
            created_at__range=(start_date, end_date),
            sale__product__category__name=category,
        ).aggregate(Sum("shipment_cost"))

        return shipment_cost["shipment_cost__sum"] or 0

    @classmethod
    def get_shipment_by_sale(cls, id_sale):
        return (
            Shipment.objects.filter(sale=id_sale)
            .values(
                "id",
                "sale",
                destination=F("departament"),
                shipping_cost=F("shipment_cost"),
            )
            .all()
        )
