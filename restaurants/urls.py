from django.urls import path
from .views import FavoriteListCreateView, UserDetailView,CreateRestaurant, RetrieveUpdateDestroyRestaurant

urlpatterns = [
    path('create/', CreateRestaurant.as_view()),
    path('update/<int:pk>/', RetrieveUpdateDestroyRestaurant.as_view()),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
]

