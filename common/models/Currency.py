from django.db import models
from enum import Enum


class CurrencyOptions(Enum):
    USD = 'usd'
    GBP = 'gbp'


class Currency(models.Model):
    value = models.TextField(
        max_length=5,
        unique=True,
        choices=[(tag, tag.value) for tag in CurrencyOptions]
    )

    @classmethod
    def list(cls):
        return [tag.value for tag in CurrencyOptions]

    class Meta:
        db_table = "currency"
