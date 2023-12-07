from django.db import models
from django.db.models import Sum


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
    minimum_stock = models.DecimalField(max_digits=3, decimal_places=0)


class HistoryPrice(models.Model):
    class Meta:
        db_table = 'history_prices'
        verbose_name = 'history_price'
        verbose_name_plural = 'history_prices'

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)


class Category(models.Model):
    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Stock(models.Model):
    class Meta:
        db_table = 'stocks'
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'

    product = models.ManyToManyField(Product)
    quantity = models.IntegerField()
    current_quantity = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @classmethod
    def get_current_quantity_by_product_category(cls, category: str) -> int:
        stock = Stock.objects.filter(product__category__name=category)\
            .aggregate(Sum('current_quantity'), Sum('quantity'))

        current_quantity = stock['current_quantity__sum'] or 0
        quantity = stock['quantity__sum'] or 0
        return current_quantity, quantity

    @classmethod
    def update_stock(cls, id: int, amount: int) -> bool:
        stock = cls.objects.get(id=id)
        if amount > stock.current_quantity:
            return False
        stock.current_quantity -= amount
        stock.save()
        return True
