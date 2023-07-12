from django.db import models


class Sel(models.Model):
    class Meta:
        db_table = 'sels'
        verbose_name = 'sel'
        verbose_name_plural = 'sels'

    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('qr', 'Qr'),
        ('transfer', 'Transfer')
    )

    seller = models.ForeignKey('sellers.Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
