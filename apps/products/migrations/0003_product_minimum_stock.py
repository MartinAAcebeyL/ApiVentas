# Generated by Django 4.2.2 on 2023-11-20 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_stock_product_stock_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='minimum_stock',
            field=models.DecimalField(decimal_places=0, default=5, max_digits=3),
        ),
    ]
