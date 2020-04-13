from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.parameters import get_number_parameter
from auctions.models.Auction import Auction
from auctions.models.AuctionStatus import AuctionStatusOption
from auctions.models.Bid import Bid
from auctions.serializers.AuctionSerializer import AuctionSerializer
from auctions.serializers.BidSerializer import BidSerializer


class FetchAuctionView(APIView):
    """
    Fetch the details of an auction

    If this auction has been fulfilled, the winning bid is also appended.
    """

    def get(self, request, auction_id):
        auction_id = get_number_parameter({'auction_id': auction_id}, 'auction_id', int, True)
        auction = Auction.objects.filter(id=auction_id).first()

        if auction is None:
            raise Http404()

        bid = None
        if auction.status.value == AuctionStatusOption.FULFILLED.value:
            winning_bid = Bid.objects.filter(auction=auction, is_winning_bid=True).first()
            if winning_bid:
                # No auction as it is redundant.
                bid = BidSerializer(winning_bid, fields=['bid_amount', 'bid_currency', 'user', 'bid_time_utc'])

        serializer = AuctionSerializer(auction)
        response = serializer.data
        if bid:
            response['winning_bid'] = bid.data
        return Response(response)
