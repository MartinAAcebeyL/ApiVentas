# Generated by Django 4.2.2 on 2024-01-13 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ManyToManyField(related_name='sale_products', to='products.product')),
            ],
            options={
                'verbose_name': 'sale',
                'verbose_name_plural': 'sales',
                'db_table': 'sales',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departament', models.CharField(choices=[('La Paz', 'La Paz'), ('Cochabamba', 'Cochabamba'), ('Santa Cruz', 'Santa Cruz'), ('Oruro', 'Oruro'), ('Potosi', 'Potosi'), ('Tarija', 'Tarija'), ('Beni', 'Beni'), ('Pando', 'Pando'), ('Chuquisaca', 'Chuquisaca')], max_length=12)),
                ('city', models.CharField(default='Sucre', max_length=255)),
                ('shipment_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_transit', 'In transit'), ('delivered', 'Delivered')], max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('sale', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
            ],
            options={
                'verbose_name': 'shipment',
                'verbose_name_plural': 'shipments',
                'db_table': 'shipments',
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('qr', 'Qr'), ('transfer', 'Transfer')], max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('sale', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
            ],
            options={
                'verbose_name': 'sale_detail',
                'verbose_name_plural': 'sales_details',
                'db_table': 'sales_details',
            },
        ),
    ]
