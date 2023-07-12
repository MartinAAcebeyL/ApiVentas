from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    