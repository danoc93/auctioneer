import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.environment import OAUTH_TOKEN_URL, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
from common.utils.parameters import get_string_parameter

request_schema = openapi.Schema(
    type="object",
    required=['refresh_token'],
    properties={
        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
    }
)


class RefreshTokenView(APIView):
    """
    Refresh an authorization token and return the refreshed version.

    This endpoint will only refresh tokens if the user is logged.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The token metadata',
            '401': 'Invalid credentials',
            '403': 'Invalid login'
        },
        request_body=request_schema
    )
    def post(self, request):
        refresh_token = get_string_parameter(request.data, 'refresh_token', True)

        # Attempt to refresh via the provider.
        r = requests.post(
            OAUTH_TOKEN_URL,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': OAUTH_CLIENT_ID,
                'client_secret': OAUTH_CLIENT_SECRET,
            },
        )
        return Response(r.json())
