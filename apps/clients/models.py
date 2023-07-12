from apps.users.models import User
# Create your models here.
class Clients(User):
    class Meta:
        db_table = 'clients'
        verbose_name = 'client'
        verbose_name_plural = 'clients'