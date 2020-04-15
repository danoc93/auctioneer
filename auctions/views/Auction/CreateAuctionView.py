from datetime import datetime

from django.core.exceptions import SuspiciousOperation
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.parameters import get_datetime_parameter, get_string_parameter, get_boolean_parameter, \
    get_number_parameter, get_enum_parameter
from auctions.models.Auction import Auction
from auctions.models.AuctionStatus import AuctionStatus
from auctions.models.Currency import Currency
from auctions.models.Item import Item
from auctions.models.ItemCondition import ItemCondition
from user_auth.models.User import User

request_schema = openapi.Schema(
    type="object",
    required=['expiration_date_utc', 'status', 'ask_amount_currency', 'starting_ask_amount', 'international_delivery',
              'item'],
    properties={
        'expiration_time_utc': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
        'status': openapi.Schema(type=openapi.TYPE_STRING, enum=AuctionStatus.list()),
        'ask_amount_currency': openapi.Schema(type=openapi.TYPE_STRING, enum=Currency.list()),
        'starting_ask_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
        'international_delivery': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'item': openapi.Schema(type=openapi.TYPE_OBJECT,
                               required=['title', 'description', 'condition'],
                               properties={
                                   'title': openapi.Schema(type=openapi.TYPE_STRING),
                                   'description': openapi.Schema(type=openapi.TYPE_STRING),
                                   'condition': openapi.Schema(type=openapi.TYPE_STRING, enum=ItemCondition.list())
                               }),
    }
)


class CreateAuctionView(APIView):
    """
    Auction a new item

    This endpoint can be used to open an auction.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The id of the created auction'
        },
        request_body=request_schema,
        tags=['auction']
    )
    def post(self, request):
        current_user_id = request.user.id

        expiration_time_utc = get_datetime_parameter(request.data, 'expiration_time_utc', True)
        if expiration_time_utc < datetime.now():
            raise SuspiciousOperation('Auction expiration date cannot be in the past.')
        ask_amount_currency = Currency.objects.filter(
            value=get_string_parameter(request.data, 'ask_amount_currency', True)
        ).first()
        international_delivery = get_boolean_parameter(request.data, 'international_delivery')
        starting_ask_amount = get_number_parameter(request.data, 'starting_ask_amount', float, True)

        if starting_ask_amount < 0:
            raise SuspiciousOperation('Negative ask amounts are not allowed.')

        status = AuctionStatus.objects.filter(
            value=get_enum_parameter(request.data, 'status', ['open', 'closed'], True)
        ).first()

        item = request.data.get('item', {})
        title = get_string_parameter(item, 'title', True)
        description = get_string_parameter(item, 'description', True)
        condition = ItemCondition.objects.filter(
            value=get_enum_parameter(item, 'condition', ItemCondition.list(), True)
        ).first()

        owner = User.objects.filter(id=current_user_id).first()

        item = Item(**{
            'owner': owner,
            'title': title,
            'description': description,
            'condition': condition
        })

        auction = Auction(**{
            'ask_amount_currency': ask_amount_currency,
            'international_delivery': international_delivery,
            'expiration_time_utc': expiration_time_utc,
            'starting_ask_amount': starting_ask_amount,
            'status': status,
            'item': item
        })

        item.save()
        auction.save()

        return Response({'auction_id': auction.id})
