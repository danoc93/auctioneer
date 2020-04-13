from user_auth.models.User import User
from auctions.serializers.CountrySerializer import CountrySerializer
from auctions.serializers.CustomFieldsModelSerializer import CustomFieldsModelSerializer


class UserSerializer(CustomFieldsModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = User
        fields = '__all__'
