from django.db import models


class Sale(models.Model):
    class Meta:
        db_table = 'sales'
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('qr', 'Qr'),
        ('transfer', 'Transfer')
    )

    seller = models.ForeignKey('sellers.Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SaleDetail(models.Model):
    class Meta:
        db_table = 'sales_details'
        verbose_name = 'sale_detail'
        verbose_name_plural = 'sales_details'

    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
