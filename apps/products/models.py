from django.db import models


class Product(models.Model):
    class Meta:
        db_table = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Category(models.Model):
    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Stock(models.Model):
    class Meta:
        db_table = 'stocks'
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
