# Generated by Django 4.2.2 on 2023-07-14 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellers', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.seller'),
        ),
    ]
