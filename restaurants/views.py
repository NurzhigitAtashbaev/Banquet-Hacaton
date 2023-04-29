from rest_framework import generics, permissions
from rest_framework.mixins import CreateModelMixin
from .models import Restaurant, Favorite
from applications.account.models import CustomUser
from .serializers import RestaurantSerializer, FavoriteSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser

# class RestaurantFilter(filters_.FilterSet):
#     name = filters_.CharFilter(field_name='name', lookup_expr='istartswith')
#
#     class Meta:
#         model = Restaurant
#         fields = ['name']


# class RestaurantListView(ListAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [filters.DjangoFilterBackend]
#     filterset_class = RestaurantFilter


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


class AddToFavorite(generics.GenericAPIView, CreateModelMixin):
    #permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FavoriteList(ListAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class RemoveFromFavorite(DestroyAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()