from rest_framework.response import Response
from rest_framework.views import APIView

from common.models.Currency import Currency
from common.serializers.CurrencySerializer import CurrencySerializer


class FetchCurrenciesView(APIView):
    """
    Fetch the list of supported currencies.
    """

    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)
