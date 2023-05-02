import django_filters
from rest_framework import views, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView, \
    ListAPIView, GenericAPIView, DestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from .models import Restaurants, Favorite, Comment
from .permissions import IsBusinessUser
from .serializers import RestaurantSerializer, FavoriteSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class RestaurantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Restaurants
        fields = ['name']


class RestaurantListView(ListAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
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
    #permission_classes = [IsAuthenticated]
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