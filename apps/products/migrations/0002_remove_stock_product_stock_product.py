# Generated by Django 4.2.2 on 2023-07-14 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='product',
        ),
        migrations.AddField(
            model_name='stock',
            name='product',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]