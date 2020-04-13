from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.parameters import get_enum_parameter, get_number_parameter
from auctions.models.Auction import Auction
from auctions.models.AuctionStatus import AuctionStatus, AuctionStatusOption
from auctions.models.Item import Item
from user_auth.models.User import User
from auctions.serializers.AuctionSerializer import AuctionSerializer

from datetime import datetime


class FetchAllAuctionsView(APIView):
    """
    Fetch all auctions based on their status

    This endpoint retrieves a list of public auctions
    """

    @swagger_auto_schema(
        responses={
            '200': 'The list of available auctions for the provided filters',
            '404': 'Provided owner not found'
        },
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              enum=AuctionStatus.list()),
            openapi.Parameter('owner_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):
        owner_id = get_number_parameter(request.query_params, 'owner_id', int)
        status_key = get_enum_parameter(request.query_params, 'status', AuctionStatus.list())

        owner = None
        if owner_id:
            owner = User.objects.filter(id=owner_id).first()
            if not owner:
                raise Http404()

        if status_key == AuctionStatusOption.OPEN.value:
            status_entity = AuctionStatus.objects.filter(value=status_key).first()
            auction_items = Auction.objects.filter(status=status_entity, expiration_time_utc__gt=datetime.now())
        elif status_key:
            status_entity = AuctionStatus.objects.filter(value=status_key).first()
            auction_items = Auction.objects.filter(status=status_entity)
        else:
            auction_items = Auction.objects.all()

        if owner:
            items = Item.objects.filter(owner=owner)
            auction_items = auction_items.filter(item__in=items)

        serializer = AuctionSerializer(auction_items, many=True)
        return Response(serializer.data)
