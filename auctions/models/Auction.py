from django.db import models

from auctions.models.Item import Item
from auctions.models.AuctionStatus import AuctionStatus
from auctions.models.Currency import Currency


class Auction(models.Model):
    starting_ask_amount = models.FloatField(default=0, null=False)
    ask_amount_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=False)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=False)
    status = models.ForeignKey(AuctionStatus, on_delete=models.PROTECT, null=False)
    expiration_time_utc = models.DateTimeField(null=False)
    international_delivery = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "auction"
