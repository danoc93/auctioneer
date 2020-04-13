from rest_framework.response import Response
from rest_framework.views import APIView

from common.models.ItemCondition import ItemCondition
from common.serializers.ItemConditionSerializer import ItemConditionSerializer


class FetchItemConditionsView(APIView):
    """
    Fetch the list of supported item conditions.
    """

    def get(self, request):
        conditions = ItemCondition.objects.all()
        serializer = ItemConditionSerializer(conditions, many=True)
        return Response(serializer.data)
