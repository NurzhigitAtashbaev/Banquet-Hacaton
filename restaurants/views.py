import django_filters
from rest_framework import views
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView, GenericAPIView, DestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from .models import Restaurants, Favorite, Comment, Rating
from .permissions import IsBusinessUser
from .serializers import RestaurantSerializer, FavoriteSerializer, CommentSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import ModelMultipleChoiceFilter
from django.db.models import Avg


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100000


class RestaurantFilter(django_filters.FilterSet):
    locate = django_filters.CharFilter(lookup_expr='icontains')
    min_rating = django_filters.NumberFilter(method='filter_min_rating', label='Рейтинг')

    # фильтрация по рейтингу
    def filter_min_rating(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating__gte=value)

    # фильтрация по названию ресторана
    restaurants = ModelMultipleChoiceFilter(
        field_name='title',
        queryset=Restaurants.objects.all(),
        to_field_name='title',
        label='Выберите Ресторан'

    )

    # фильтрация по ценовому диапазону
    price_range = django_filters.RangeFilter(field_name='price_people')

    class Meta:
        model = Restaurants
        fields = ['restaurants', 'locate']


class RestaurantListView(ListAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    pagination_class = LargeResultsSetPagination
    filterset_class = RestaurantFilter
    search_fields = ['title']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # обработка параметра запроса search
        search = request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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


class CommentAPIView(views.APIView):
    permission_classes = [IsAuthenticated, IsBusinessUser]

    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        return Response(serializer.data, status=201)


class CommentDetailAPIView(views.APIView):
    def get_comment(self, pk):
        try:
            return Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        comment = self.get_comment(pk)
        if comment:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        return Response(status=404)

    def put(self, request, pk):
        comment = self.get_comment(pk)
        if comment:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response('такого коммента нет', status=404)

    def delete(self, request, pk):
        comment = self.get_comment(pk)
        if comment:
            comment.delete()
            return Response(status=204)
        return Response(status=404)


class RatingAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(restaurant_id=pk, user=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(restaurant_id=pk, user=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        obj, _ = Rating.objects.get_or_create(restaurant_id=pk, user=request.user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




