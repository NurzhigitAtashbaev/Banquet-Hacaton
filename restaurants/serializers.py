from rest_framework import serializers
from .models import *

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    # restaurant = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)

    class Meta:
        model = Restaurants
        fields = "__all__"