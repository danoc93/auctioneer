from rest_framework import serializers

from common.models.ItemCondition import ItemCondition


class ItemConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCondition
        fields = '__all__'
