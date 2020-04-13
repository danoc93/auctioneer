from rest_framework import serializers

from auctions.models.Country import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
