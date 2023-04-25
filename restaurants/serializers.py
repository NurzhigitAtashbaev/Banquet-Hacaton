from rest_framework import serializers
from .models import Restaurants, Favorite


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Favorite
        fields = ('restaurant',)