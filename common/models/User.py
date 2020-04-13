from django.db import models

from common.models.Country import Country


class User(models.Model):
    username = models.CharField(max_length=30, unique=True, null=False)
    email = models.CharField(max_length=60, unique=True, null=False)
    first_name = models.CharField(max_length=60, null=False)
    last_name = models.CharField(max_length=60, null=False)
    registration_date_utc = models.DateTimeField(null=False)
    city_name = models.TextField(null=False, max_length=30)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "user"


USER_PUBLIC_VIEW = ['id', 'username', 'country', 'city_name']
