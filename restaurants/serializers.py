from rest_framework import serializers

from applications.account.models import CustomUser
from .models import Restaurants, Favorite


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"




class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'