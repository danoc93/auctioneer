from auctions.models.Item import Item
from user_auth.models.User import USER_PUBLIC_VIEW
from auctions.serializers.CustomFieldsModelSerializer import CustomFieldsModelSerializer
from user_auth.serializers.UserSerializer import UserSerializer


class ItemSerializer(CustomFieldsModelSerializer):
    owner = UserSerializer(fields=USER_PUBLIC_VIEW, read_only=False)

    class Meta:
        model = Item
        fields = '__all__'
