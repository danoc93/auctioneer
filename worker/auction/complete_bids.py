import time

from django.db.models import Max
from django.utils import timezone

from auctions.models.Auction import Auction
from auctions.models.AuctionStatus import AuctionStatusOption, AuctionStatus
from auctions.models.Bid import Bid

"""
This worker fulfills expired auctions and declares winner bids.
"""


def complete_bids():
    i = 0
    while i < 10:
        check_bids()
        time.sleep(5)
        i += 1


def check_bids():
    print('Finding all expired auctions @', timezone.now())
    auctions = Auction.objects.filter(
        status__value=AuctionStatusOption.OPEN.value,
        expiration_time_utc__lte=timezone.now()
    )

    if len(auctions) == 0:
        print('No unfulfilled auctions found')
        return

    new_status = AuctionStatus.objects.filter(value=AuctionStatusOption.FULFILLED.value).first()
    for auction in auctions:
        auction.status = new_status
        auction.save()

        winning_bid_amount = Bid.objects.aggregate(Max('bid_amount'))['bid_amount__max']
        winning_bid = Bid.objects.filter(
            auction=auction, bid_amount=winning_bid_amount
        ).order_by('bid_time_utc').first()

        if winning_bid:
            winning_bid.is_winning_bid = True
            winning_bid.save()
            print('Bid {} set as winner for auction {}'.format(winning_bid.id, auction.id))
            # Here we could potentially email people.
        else:
            print('Auction {} has no winning bid'.format(auction.id))
