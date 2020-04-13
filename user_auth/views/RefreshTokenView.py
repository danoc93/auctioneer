import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from auctioneer_api.settings import OAUTH_TOKEN_URL, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
from common.utils.parameters import get_string_parameter


class RefreshTokenView(APIView):
    """
    Refresh an authorization token and return the refreshed version.

    This endpoint will only refresh tokens if the user is logged.
    """

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
