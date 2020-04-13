from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from auctioneer_api.api.parameters import get_enum_parameter
from common.models.Auction import Auction
from common.models.AuctionStatus import AuctionStatus, AuctionStatusOption
from common.serializers.AuctionSerializer import AuctionSerializer

from datetime import datetime


class FetchAllAuctionsView(APIView):
    """
    Fetch the list of available auctions.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The list of available auctions for the provided filters',
        },
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              enum=AuctionStatus.list()),
        ]
    )
    def get(self, request):
        status_key = get_enum_parameter(request.query_params, 'status', AuctionStatus.list())

        if status_key == AuctionStatusOption.OPEN.value:
            status_entity = AuctionStatus.objects.filter(value=status_key).first()
            auction_items = Auction.objects.filter(status=status_entity, expiration_time_utc__gt=datetime.now())
        elif status_key:
            status_entity = AuctionStatus.objects.filter(value=status_key).first()
            auction_items = Auction.objects.filter(status=status_entity)
        else:
            auction_items = Auction.objects.all()

        serializer = AuctionSerializer(auction_items, many=True)
        return Response(serializer.data)
