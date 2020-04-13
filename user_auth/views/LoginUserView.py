import requests
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auctioneer_api.settings import OAUTH_TOKEN_URL, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET


class LoginUserView(APIView):
    """
    Login a user with the internal OAuth Provider.
    """
    permission_classes = [AllowAny]

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
