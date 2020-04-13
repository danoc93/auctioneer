from auctions.models.Bid import Bid
from user_auth.models.User import USER_PUBLIC_VIEW
from auctions.serializers.AuctionSerializer import AuctionSerializer
from auctions.serializers.CurrencySerializer import CurrencySerializer
from auctions.serializers.CustomFieldsModelSerializer import CustomFieldsModelSerializer
from user_auth.serializers.UserSerializer import UserSerializer


class BidSerializer(CustomFieldsModelSerializer):

    bid_currency = CurrencySerializer()
    user = UserSerializer(fields=USER_PUBLIC_VIEW)
    auction = AuctionSerializer()

    class Meta:
        model = Bid
        fields = '__all__'
