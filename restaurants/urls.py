from django.urls import path, include
from .views import (AddToFavorite, CreateRestaurant, RetrieveUpdateDestroyRestaurant, FavoriteList, RemoveFromFavorite,
                    RestaurantListView, CommentAPIView, CommentDetailAPIView)

urlpatterns = [
    path('all/', RestaurantListView.as_view(), name='restaurant-list'),
    path('create/', CreateRestaurant.as_view()),
    path('update/<int:pk>/', RetrieveUpdateDestroyRestaurant.as_view()),
    path('add-to-favorite/', AddToFavorite.as_view(), name='add-to-favorite'),
    path('favorites/', FavoriteList.as_view(), name='favorite-list'),
    path('remove-favorite/<int:pk>', RemoveFromFavorite.as_view(), name='remove-from-favorite'),
    path('comment/', CommentAPIView.as_view(), name='comment-list-create'),
    path('comment-detail/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail')
]