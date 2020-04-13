from rest_framework import serializers

from common.models.Auction import Auction
from common.serializers.AuctionStatusSerializer import AuctionStatusSerializer
from common.serializers.CurrencySerializer import CurrencySerializer
from common.serializers.ItemSerializer import ItemSerializer


class AuctionSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    status = AuctionStatusSerializer()
    ask_amount_currency = CurrencySerializer()

    class Meta:
        model = Auction
        fields = '__all__'
