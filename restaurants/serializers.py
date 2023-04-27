from rest_framework import serializers

from applications.account.models import CustomUser
from .models import Restaurants


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"


