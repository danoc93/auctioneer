from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from auctions.models.Item import Item
from auctions.serializers.ItemSerializer import ItemSerializer


class FetchMemberItemsView(APIView):
    """
    Fetch the items added by the current member

    This endpoint lists all items created by the member, not necessarily all of them have been auctioned.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The list of items added by the member',
        },
        tags=['member']
    )
    def get(self, request):
        current_user_id = request.user.id

        items = Item.objects.filter(owner_id=current_user_id).order_by('registration_date_utc')
        item_serializer = ItemSerializer(items, many=True,
                                         fields=['id', 'title', 'description', 'registration_date_utc', 'condition'])
        return Response(item_serializer.data)
