from django.db import models
from enum import Enum


class AuctionStatusOption(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    FULFILLED = 'fulfilled'


class AuctionStatus(models.Model):
    value = models.TextField(
        max_length=20,
        unique=True,
        choices=[(tag, tag.value) for tag in AuctionStatusOption]
    )

    @classmethod
    def list(cls):
        return [tag.value for tag in AuctionStatusOption]

    class Meta:
        db_table = "auction_status"
