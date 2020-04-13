from django.db import models
from django.utils import timezone

from common.models.ItemCondition import ItemCondition
from common.models.User import User


class Item(models.Model):
    title = models.TextField(max_length=125, null=False)
    description = models.TextField(max_length=5000, null=False)
    registration_date_utc = models.DateTimeField(default=timezone.now, null=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    condition = models.ForeignKey(ItemCondition, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "item"
