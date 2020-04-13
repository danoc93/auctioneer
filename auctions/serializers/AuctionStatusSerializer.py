from rest_framework import serializers

from auctions.models.AuctionStatus import AuctionStatus


class AuctionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionStatus
        fields = '__all__'
