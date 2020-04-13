from django.db import models
from enum import Enum


class ItemConditionOptions(Enum):
    NEW = 'new'
    USED = 'used'


class ItemCondition(models.Model):
    value = models.TextField(
        max_length=20,
        unique=True,
        choices=[(tag, tag.value) for tag in ItemConditionOptions]
    )

    @classmethod
    def list(cls):
        return [tag.value for tag in ItemConditionOptions]

    class Meta:
        db_table = "item_condition"
