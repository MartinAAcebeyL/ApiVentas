# Generated by Django 4.2.2 on 2023-07-14 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_stock_product_stock_product'),
        ('sales', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='product',
        ),
        migrations.AlterField(
            model_name='saledetail',
            name='sale',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.sale'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='sale',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.sale'),
        ),
        migrations.AddField(
            model_name='sale',
            name='product',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]
