from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.products.models import Product, Stock
from apps.utils.send_emails import send_email
from .models import Sale

import os


@receiver(m2m_changed, sender=Sale.product.through)
def check_minimum_stock(sender, instance, action, **kwargs):
    if action == 'post_add':
        products_ids = kwargs.get('pk_set')
        for product_id in products_ids:
            product = Product.objects.filter(id=product_id).first()
            current_stock = Stock.objects.filter(
                product=product.id).first().current_quantity

            if current_stock <= product.minimum_stock:
                subject = f'¡Alerta! Ya supero el valor minimo de stock de {product.minimum_stock}'
                message = f'El producto {product.name} esta en su ultimas {current_stock} unidades y debe ver de pedir mas unidades o no.'
                from_email = os.getenv('EMAIL_HOST_USER')
                to_email = ['martinaacbyl2000@gmail.com']
                send_email(message, from_email, to_email, subject)
