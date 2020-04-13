from django.db import models

from common.models.Auction import Auction
from common.models.Currency import Currency
from common.models.User import User


class Bid(models.Model):
    bid_amount = models.FloatField(null=False)
    bid_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    bid_time_utc = models.DateTimeField(null=False)
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT, null=False)
    is_winning_bid = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "bid"
