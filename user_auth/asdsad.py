from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests

from auctioneer_api.settings import OAUTH_TOKEN_URL, OAUTH_CLIENT_SECRET, OAUTH_CLIENT_ID, OAUTH_TOKEN_REVOKE_URL
from user_auth.serializers.UserSerializer import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer 
    serializer = UserSerializer(data=request.data)
    # Validate the data
    if serializer.is_valid(raise_exception=True):
        # If it is valid, save the data (creates a user).
        serializer.save()
        # Then we get a token for the created user.
        # This could be done differentley 
        r = requests.post(OAUTH_TOKEN_URL,
                          data={
                              'grant_type': 'password',
                              'username': request.data['username'],
                              'password': request.data['password'],
                              'client_id': OAUTH_CLIENT_ID,
                              'client_secret': OAUTH_CLIENT_SECRET,
                          },
                          )
        return Response(r.json())
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
        OAUTH_TOKEN_URL,
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
        OAUTH_TOKEN_URL,
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        OAUTH_TOKEN_REVOKE_URL,
        data={
            'token': request.data['token'],
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise) 
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
