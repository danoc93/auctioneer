import requests
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.environment import OAUTH_TOKEN_URL, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
from auctions.models.Country import Country
from user_auth.models.User import User


class RegisterUserView(APIView):
    """
    Register a user with the internal OAuth Provider.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # Current metadata
        data['country'] = Country.objects.filter(id=data['country']).first()

        if not data.get('country', None) or not data.get('city_name', None):
            return Response('Fields country and city_name are required.', 400)

        data['is_superuser'] = False
        data['is_staff'] = False
        data['is_active'] = True

        # Validate the data
        try:
            user = User.objects.create_user(**data)
            user.save()
        except IntegrityError as e:
            return Response('Unable to create user, it already exists.', 409)

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
