from rest_framework import generics, permissions
from .models import Restaurant
from applications.account.models import CustomUser
from .serializers import RestaurantSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser


class CreateRestaurant(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]

    def perform_create(self, serializer):
        serializer.save(business=self.request.user)  # Сохранение ресторана с указанием пользователя


class RetrieveUpdateDestroyRestaurant(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]


class FavoriteListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(fans=[self.request.user])


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


