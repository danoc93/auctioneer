from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.models.User import User, USER_PRIVATE_VIEW
from user_auth.serializers.UserSerializer import UserSerializer


class FetchMemberView(APIView):
    """
    Fetch the member details

    This endpoint lists all the account information related to the current member
    """

    @swagger_auto_schema(
        responses={
            '200': 'The member public view',
        }
    )
    def get(self, request):
        current_user_id = request.user.id

        user_serializer = UserSerializer(User.objects.filter(id=current_user_id).first(), fields=USER_PRIVATE_VIEW)

        return Response(user_serializer.data)
