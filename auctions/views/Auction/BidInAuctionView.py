from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.parameters import get_string_parameter, get_number_parameter
from auctions.models.Auction import Auction
from auctions.models.AuctionStatus import AuctionStatusOption
from auctions.models.Bid import Bid
from auctions.models.Currency import Currency
from user_auth.models.User import User

request_schema = openapi.Schema(
    type="object",
    required=['bid_amount', 'bid_currency'],
    properties={
        'bid_currency': openapi.Schema(type=openapi.TYPE_STRING, enum=Currency.list()),
        'bid_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
    }
)


class BidInAuctionView(APIView):
    """
    Bid for an auctioned item

    This endpoint can be used to bid on an open auction.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The id of the created bid record',
            '400': 'The action is not valid/request is invalid',
            '404': 'The provided auction does not exist'
        },
        request_body=request_schema,
        tags=['auction']
    )
    def post(self, request, auction_id):

        current_user_id = request.user.id

        auction_id = get_number_parameter({'auction_id': auction_id}, 'auction_id', int, True)
        auction = Auction.objects.filter(id=auction_id).first()

        now = timezone.now()
        if auction is None:
            raise Http404()
        expiration_time_utc = auction.expiration_time_utc
        if expiration_time_utc is None or expiration_time_utc < now \
                or auction.status.value != AuctionStatusOption.OPEN.value:
            raise SuspiciousOperation('This auction is not available for bidding.')

        bidder = User.objects.filter(id=current_user_id).first()
        if bidder == auction.item.owner:
            raise SuspiciousOperation('Not allowed to bid on own auctions.')

        bid_currency = Currency.objects.filter(
            value=get_string_parameter(request.data, 'bid_currency', True)
        ).first()
        if bid_currency != auction.ask_amount_currency:
            raise SuspiciousOperation('Bidding can only happen in the same currency.')

        bid_amount = get_number_parameter(request.data, 'bid_amount', float, True)
        if bid_amount < auction.starting_ask_amount:
            raise SuspiciousOperation('Bid lower than minimum value.')

        bid = Bid(**{
            'auction': auction,
            'user': bidder,
            'bid_time_utc': now,
            'bid_amount': bid_amount,
            'bid_currency': bid_currency
        })

        bid.save()

        return Response({'auction_id': auction.id, 'bid_id': bid.id})
