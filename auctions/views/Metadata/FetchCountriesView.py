from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from auctions.models.Country import Country
from auctions.serializers.CountrySerializer import CountrySerializer


class FetchCountriesView(APIView):
    """
    List of supported countries

    These values can be passed to different operations.
    """

    @swagger_auto_schema(
        responses={
            '200': 'The requested metadata',
        },
        tags=['metadata']
    )
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)
