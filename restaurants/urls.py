from django.urls import path
from .views import CreateRestaurant, RetrieveUpdateDestroyRestaurant, FavoriteListCreateView

urlpatterns = [
    path('create/', CreateRestaurant.as_view()),
    path('update/<int:pk>/', RetrieveUpdateDestroyRestaurant.as_view()),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
]
