import django_filters
from django import forms
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView, \
    ListAPIView, GenericAPIView, DestroyAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Restaurant, Favorite, Rating, Comment
from .permissions import IsBusinessUser
from .serializers import (RestaurantSerializer, FavoriteSerializer, RatingSerializer, CommentSerializer)


class CharFilterInFilter(django_filters.BaseInFilter, django_filters.CharFilter, django_filters.NumberFilter):
    pass


PRICE_CHOICES = (
    ('', '___________'),
    ('1', '1000-1500'),
    ('2', '1500-2000'),
    ('3', '2000-3000'),
    ('4', 'До  3000')
)


class RestaurantFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='istartswith')
    price_people = django_filters.CharFilter(field_name='price_people', lookup_expr='lte',
                                             widget=forms.Select(choices=PRICE_CHOICES), required=False)

    class Meta:
        model = Restaurant
        fields = ['title', 'price_people']


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


class RetrieveUpdateDestroyRestaurant(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]


class CreateRating(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]  # Добавляем разрешение для аутентифицированных пользователей

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class CommentAPIView(APIView):
    def get(self, request):
        serializer = CommentSerializer(many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    def get_comment(self, comment_id):
        try:
            return Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return None

    def get(self, request, comment_id):
        comment = self.get_comment(comment_id)
        if comment:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, comment_id):
        comment = self.get_comment(comment_id)
        if comment:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, comment_id):
        comment = self.get_comment(comment_id)
        if comment:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
