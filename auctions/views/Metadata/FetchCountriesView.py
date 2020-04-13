from rest_framework.response import Response
from rest_framework.views import APIView

from common.models.Country import Country
from common.serializers.CountrySerializer import CountrySerializer


class FetchCountriesView(APIView):
    """
    Fetch the list of supported countries.
    """

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)
