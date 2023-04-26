from django.urls import path
from .views import FavoriteListCreateView, UserDetailView

urlpatterns = [
    path('favorites/', FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
]