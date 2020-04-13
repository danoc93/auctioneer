from rest_framework.response import Response
from rest_framework.views import APIView

from auctions.models.ItemCondition import ItemCondition
from auctions.serializers.ItemConditionSerializer import ItemConditionSerializer


class FetchItemConditionsView(APIView):
    """
    List of supported item conditions.

    These values can be passed to different operations.
    """

    def get(self, request):
        conditions = ItemCondition.objects.all()
        serializer = ItemConditionSerializer(conditions, many=True)
        return Response(serializer.data)
