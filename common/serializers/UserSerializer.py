from rest_framework import serializers

from common.models.User import User
from common.serializers.CountrySerializer import CountrySerializer
from common.serializers.CustomFieldsModelSerializer import CustomFieldsModelSerializer


class UserSerializer(CustomFieldsModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = User
        fields = '__all__'
