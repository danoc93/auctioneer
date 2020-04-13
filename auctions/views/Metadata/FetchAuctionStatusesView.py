from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models.AuctionStatus import AuctionStatus
from common.serializers.AuctionStatusSerializer import AuctionStatusSerializer


class FetchAuctionStatusesView(APIView):
    """
    Fetch the list of supported auction status values.
    """

    def get(self, request):
        states = AuctionStatus.objects.all()
        serializer = AuctionStatusSerializer(states, many=True)
        return Response(serializer.data)
