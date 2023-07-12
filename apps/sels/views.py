from django.db import models


class Sel(models.Model):
    class Meta:
        db_table = 'sels'
        verbose_name = 'sel'
        verbose_name_plural = 'sels'

    seller = models.ForeignKey('sellers.Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
