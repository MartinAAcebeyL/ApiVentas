from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Sale
from apps.products.models import Product, Stock


@receiver(m2m_changed, sender=Sale.product.through)
def check_minimum_stock(sender, instance, action, **kwargs):
    if action == 'post_add':
        products_ids = kwargs.get('pk_set')
        for product_id in products_ids:
            product = Product.objects.filter(id=product_id).first()
            current_stock = Stock.objects.filter(
                product=product.id).first()
            print(dir(current_stock))

            # minimum_stock = product.stock.through.stock.minimum_stock
            # print(minimum_stock)
            if 5 < 6:
                pass

    # print(product)
    # if instance.minimum_stock < 5:
    #     subject = '¡Alerta! Valor numérico menor a 5'
    #     message = f'El valor numérico actual es {instance.campo_numerico}.'
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     to_email = 'destinatario@example.com'
    #     send_mail(subject, message, from_email, [to_email])
