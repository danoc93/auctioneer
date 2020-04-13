from rest_framework import serializers

from auctions.models.Auction import Auction
from auctions.serializers.AuctionStatusSerializer import AuctionStatusSerializer
from auctions.serializers.CurrencySerializer import CurrencySerializer
from auctions.serializers.ItemSerializer import ItemSerializer


class AuctionSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    status = AuctionStatusSerializer()
    ask_amount_currency = CurrencySerializer()

    class Meta:
        model = Auction
        fields = '__all__'
