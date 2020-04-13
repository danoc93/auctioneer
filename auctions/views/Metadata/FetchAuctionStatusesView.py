from rest_framework.response import Response
from rest_framework.views import APIView

from auctions.models.AuctionStatus import AuctionStatus
from auctions.serializers.AuctionStatusSerializer import AuctionStatusSerializer


class FetchAuctionStatusesView(APIView):
    """
    List of supported Auction Status values

    These values can be passed to different operations.
    """

    def get(self, request):
        states = AuctionStatus.objects.all()
        serializer = AuctionStatusSerializer(states, many=True)
        return Response(serializer.data)
