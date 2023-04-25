from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Favorite, Restaurants
from .serializers import FavoriteSerializer


class FavoriteView(APIView):
    def post(self, request, restaurant_id):
        user = request.user
        restaurant = Restaurants.objects.get(id=restaurant_id)
        favorite, created = Favorite.objects.get_or_create(user=user, restaurant=restaurant)
        if created:
            return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already in favorites'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, restaurant_id):
        user = request.user
        restaurant = Restaurants.objects.get(id=restaurant_id)
        favorite = Favorite.objects.filter(user=user, restaurant=restaurant).first()
        if favorite:
            favorite.delete()
            return Response({'detail': 'Removed from favorites'})
        return Response({'detail': 'Not in favorites'}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteListView(APIView):
    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)