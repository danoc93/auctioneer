from django.db import models

from auctioneer_api import settings
from auctions.models.Auction import Auction
from auctions.models.Currency import Currency


class Bid(models.Model):
    bid_amount = models.FloatField(null=False)
    bid_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False)
    bid_time_utc = models.DateTimeField(null=False)
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT, null=False)
    is_winning_bid = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "bid"
