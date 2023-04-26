from rest_framework import serializers
from .models import Restaurant
from applications.account.models import CustomUser


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    favorites = RestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'favorites']