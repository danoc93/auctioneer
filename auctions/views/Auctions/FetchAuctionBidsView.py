from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from auctioneer_api.api.parameters import get_number_parameter
from common.models.Auction import Auction
from common.models.Bid import Bid
from common.serializers.AuctionSerializer import AuctionSerializer
from common.serializers.BidSerializer import BidSerializer


class FetchAuctionBidsView(APIView):
    """
    Fetch an auction's bidding history.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The list of available bids for the provided auction',
            '404': 'The provided auction does not exist'
        }
    )
    def get(self, request, auction_id):
        auction_id = get_number_parameter({'auction_id': auction_id}, 'auction_id', int, True)
        auction = Auction.objects.filter(id=auction_id).first()

        if auction is None:
            raise Http404()

        bids = Bid.objects.filter(auction=auction).order_by('bid_time_utc')
        serializer = BidSerializer(bids, many=True, fields=['id', 'bid_currency', 'user', 'bid_amount', 'bid_time_utc',
                                                            'is_winning_bid'])
        auction_serializer = AuctionSerializer(auction)

        return Response({"auction": auction_serializer.data, "bids": serializer.data})
