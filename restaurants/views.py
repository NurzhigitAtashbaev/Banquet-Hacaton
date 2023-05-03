import django_filters
from django import forms
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from .models import Restaurant, Favorite
from .serializers import RestaurantSerializer, FavoriteSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, DestroyAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser


class CharFilterInFilter(django_filters.BaseInFilter, django_filters.CharFilter, django_filters.NumberFilter):
    pass


PRICE_CHOICES = (
    ('', '___________'),
    ('1', '1000-1500'),
    ('2', '1500-2000'),
    ('3', '2000-3000'),
    ('4', 'Более 3000')
)


class RestaurantFilter(django_filters.FilterSet):
    # category__name = CharFilterInFilter(field_name='category__name', lookup_expr='in')
    name = django_filters.CharFilter(field_name='name', lookup_expr='istartswith')
    price_people = django_filters.NumberFilter(field_name='price_people', lookup_expr='lte',
                                               widget=forms.Select(choices=PRICE_CHOICES), required=False)

    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'price_people']


class RestaurantListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RestaurantFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # обработка параметра запроса search
        search = request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
