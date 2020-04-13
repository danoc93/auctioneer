from django.contrib.auth.models import AbstractUser
from django.db import models

from auctions.models.Country import Country


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, null=False)
    email = models.CharField(max_length=60, unique=True, null=False)
    city_name = models.TextField(null=False, max_length=30)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "user"


USER_PUBLIC_VIEW = ['id', 'username', 'country', 'city_name']
USER_PRIVATE_VIEW = ['id', 'username', 'country', 'city_name', 'first_name', 'last_name', 'date_joined',
                     'email']
