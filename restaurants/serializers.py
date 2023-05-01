from rest_framework import serializers
<<<<<<< HEAD
from .models import Restaurant, Favorite
=======

from applications.account.models import CustomUser
from .models import Restaurants, Favorite
>>>>>>> master


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


<<<<<<< HEAD
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
=======


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
>>>>>>> master
