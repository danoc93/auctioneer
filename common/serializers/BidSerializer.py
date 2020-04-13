from common.models.Bid import Bid
from common.models.User import USER_PUBLIC_VIEW
from common.serializers.AuctionSerializer import AuctionSerializer
from common.serializers.CurrencySerializer import CurrencySerializer
from common.serializers.CustomFieldsModelSerializer import CustomFieldsModelSerializer
from common.serializers.UserSerializer import UserSerializer


class BidSerializer(CustomFieldsModelSerializer):

    bid_currency = CurrencySerializer()
    user = UserSerializer(fields=USER_PUBLIC_VIEW)
    auction = AuctionSerializer()

    class Meta:
        model = Bid
        fields = '__all__'
