from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Restaurants
from .serializers import RestaurantSerializer


class CreateRestaurant(CreateAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer


class RetrieveUpdateDestroyRestaurant(RetrieveUpdateDestroyAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
