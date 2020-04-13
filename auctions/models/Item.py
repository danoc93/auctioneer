from django.db import models
from django.utils import timezone

from auctioneer_api import settings
from auctions.models.ItemCondition import ItemCondition


class Item(models.Model):
    title = models.TextField(max_length=125, null=False)
    description = models.TextField(max_length=5000, null=False)
    registration_date_utc = models.DateTimeField(default=timezone.now, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False)
    condition = models.ForeignKey(ItemCondition, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "item"
