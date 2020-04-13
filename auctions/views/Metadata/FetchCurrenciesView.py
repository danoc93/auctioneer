from rest_framework.response import Response
from rest_framework.views import APIView

from auctions.models.Currency import Currency
from auctions.serializers.CurrencySerializer import CurrencySerializer


class FetchCurrenciesView(APIView):
    """
    List of supported currencies.

    These values can be passed to different operations.
    """

    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)
