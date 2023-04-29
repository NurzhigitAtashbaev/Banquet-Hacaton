from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView, \
    ListAPIView, GenericAPIView, DestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from applications.account.models import CustomUser
from .models import Restaurants, Favorite
from .permissions import IsBusinessUser
from .serializers import RestaurantSerializer, FavoriteSerializer


class CreateRestaurant(CreateAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]

    def perform_create(self, serializer):
        serializer.save(business=self.request.user)  # Сохранение ресторана с указанием пользователя


class RetrieveUpdateDestroyRestaurant(RetrieveUpdateDestroyAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]


class AddToFavorite(GenericAPIView, CreateModelMixin):
    # permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FavoriteList(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class RemoveFromFavorite(DestroyAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
