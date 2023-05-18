from rest_framework import serializers
from .models import *
from django.db.models import Avg


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    # restaurant = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    restaurant = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ('restaurant', 'rating',)


class RestaurantSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)

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


class WhatsAppContactSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        cleaned_number = ''.join(filter(str.isdigit, value))

        if not cleaned_number.isdigit() or len(cleaned_number) < 9 or len(cleaned_number) > 15:
            raise serializers.ValidationError('Invalid phone number')

        if not value.startswith('+'):
            raise serializers.ValidationError('Phone number must start with "+"')

        return cleaned_number

