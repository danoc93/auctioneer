from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.parameters import get_boolean_parameter
from auctions.models.Bid import Bid
from auctions.serializers.BidSerializer import BidSerializer


class FetchMemberBidsView(APIView):
    """
    Fetch the bidding history for the current member

    This endpoint lists all the bids done by the Auctioneer member in the session context
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('winner', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
        ],
        responses={
            '200': 'The list of available bids made by the user',
            '400': 'Invalid parameters/request',
        }
    )
    def get(self, request):
        current_user_id = 1

        winner = get_boolean_parameter(request.query_params, 'winner', False, None)

        bids = Bid.objects.filter(user_id=current_user_id)
        if winner is not None:
            bids = bids.filter(is_winning_bid=winner)
        bids = bids.order_by('bid_time_utc')

        serializer = BidSerializer(bids, many=True,
                                   fields=['id', 'bid_currency', 'bid_amount', 'bid_time_utc', 'is_winning_bid',
                                           'auction'])

        return Response(serializer.data)
