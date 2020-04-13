from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from auctioneer_api.api.parameters import get_number_parameter
from common.models.Auction import Auction
from common.serializers.AuctionSerializer import AuctionSerializer


class FetchAuctionView(APIView):
    """
    Fetch an auction details.
    """

    def get(self, request, auction_id):
        auction_id = get_number_parameter({'auction_id': auction_id}, 'auction_id', int, True)
        auction = Auction.objects.filter(id=auction_id).first()

        if auction is None:
            raise Http404()

        serializer = AuctionSerializer(auction)
        return Response(serializer.data)
