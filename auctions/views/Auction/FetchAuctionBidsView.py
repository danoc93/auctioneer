from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.parameters import get_number_parameter
from auctions.models.Auction import Auction
from auctions.models.AuctionStatus import AuctionStatusOption
from auctions.models.Bid import Bid
from auctions.serializers.AuctionSerializer import AuctionSerializer
from auctions.serializers.BidSerializer import BidSerializer


class FetchAuctionBidsView(APIView):
    """
    Fetch the bidding history for an auction

    This endpoint lists all the bids for a concluded auction.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The list of available bids for the provided auction',
            '400': 'Invalid request/Auction is not concluded',
            '404': 'The provided auction does not exist'
        },
        tags=['auction']
    )
    def get(self, request, auction_id):
        auction_id = get_number_parameter({'auction_id': auction_id}, 'auction_id', int, True)
        auction = Auction.objects.filter(id=auction_id).first()

        if auction is None:
            raise Http404()

        if auction.status.value == AuctionStatusOption.OPEN.value:
            raise SuspiciousOperation('This auction is still open.')

        bids = Bid.objects.filter(auction=auction).order_by('bid_time_utc')
        serializer = BidSerializer(bids, many=True, fields=['id', 'bid_currency', 'user', 'bid_amount', 'bid_time_utc',
                                                            'is_winning_bid'])
        auction_serializer = AuctionSerializer(auction)

        return Response({"auction": auction_serializer.data, "bids": serializer.data})
