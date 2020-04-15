import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.environment import OAUTH_TOKEN_URL, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET

request_schema = openapi.Schema(
    type="object",
    required=['username', 'password'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    }
)


class LoginUserView(APIView):
    """
    Login a user with the internal OAuth Provider.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            '200': 'The token metadata',
            '401': 'Invalid credentials',
            '403': 'Invalid login'
        },
        request_body=request_schema
    )
    def post(self, request):
        data = request.data

        if not data.get('username', None) or not data.get('password', None):
            return Response('Fields user and password are required.', 400)

        print(OAUTH_TOKEN_URL)
        # Fetch a token and pass it to the user.
        r = requests.post(
            OAUTH_TOKEN_URL,
            data={
                'grant_type': 'password',
                'username': data['username'],
                'password': data['password'],
                'client_id': OAUTH_CLIENT_ID,
                'client_secret': OAUTH_CLIENT_SECRET,
            },
        )
        return Response(r.json())
