from django.db import models


class Country(models.Model):
    name = models.TextField(max_length=30, null=False, unique=True)

    class Meta:
        db_table = "country"
