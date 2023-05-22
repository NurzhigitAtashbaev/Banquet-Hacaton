from rest_framework import serializers
from .models import *
from django.db.models import Avg

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    items = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'items', 'date_added')


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    restaurant = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ('restaurant', 'rating',)


class RestaurantImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, required=False)
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    images = RestaurantImageSerializers(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        restaurant = Restaurants.objects.create(**validated_data)

        for image in uploaded_images:
            RestaurantImage.objects.create(restaurant=restaurant, image=image)

        return restaurant

    def to_representation(self, instance):
        res = super().to_representation(instance)
        rating = Rating.objects.filter(restaurant=instance).aggregate(Avg('rating'))['rating__avg']
        if rating:
            res['rating'] = rating
        else:
            res['rating'] = 0
        return res

    class Meta:
        model = Restaurants
        fields = '__all__'


class MenuSerializers(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'

