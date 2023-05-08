from rest_framework import serializers
from .models import Restaurant, Favorite, RestaurantImage


class RestaurantImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    images = RestaurantImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Restaurant
        fields = ["category", "name", "price_people", "locate", "working_hours", "features", "images",
                  "uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        restaurant = Restaurant.objects.create(**validated_data)

        for image in uploaded_images:
            RestaurantImage.objects.create(restaurant=restaurant, image=image)

        return restaurant

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

