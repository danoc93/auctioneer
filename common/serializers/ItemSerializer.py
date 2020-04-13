from rest_framework import serializers

from common.models.Item import Item
from common.models.User import USER_PUBLIC_VIEW
from common.serializers.UserSerializer import UserSerializer


class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(fields=USER_PUBLIC_VIEW, read_only=False)

    class Meta:
        model = Item
        fields = '__all__'
