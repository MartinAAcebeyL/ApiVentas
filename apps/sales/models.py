from django.db import models


class Sale(models.Model):
    class Meta:
        db_table = 'sales'
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    seller = models.ForeignKey('sellers.Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)


class SaleDetail(models.Model):
    class Meta:
        db_table = 'sales_details'
        verbose_name = 'sale_detail'
        verbose_name_plural = 'sales_details'

    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('qr', 'Qr'),
        ('transfer', 'Transfer')
    )

    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Shipment(models.Model):
    class Meta:
        db_table = 'shipments'
        verbose_name = 'shipment'
        verbose_name_plural = 'shipments'

    DEPARTAMENT_CHOICES = (
        ('lp', 'La Paz'),
        ('cb', 'Cochabamba'),
        ('sc', 'Santa Cruz'),
        ('or', 'Oruro'),
        ('pt', 'Potosi'),
        ('tj', 'Tarija'),
        ('be', 'Beni'),
        ('pn', 'Pando'),
        ('ch', 'Chuquisaca')
    )

    ESTATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In transit'),
        ('delivered', 'Delivered')
    )

    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    departament = models.CharField(max_length=2, choices=DEPARTAMENT_CHOICES)
    city = models.CharField(max_length=255, default='Sucre')
    shipment_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ESTATUS_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
