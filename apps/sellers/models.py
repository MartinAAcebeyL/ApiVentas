from apps.users.models import User


class Seller(User):
    class Meta:
        db_table = 'sellers'
        verbose_name = 'seller'
        verbose_name_plural = 'sellers'
