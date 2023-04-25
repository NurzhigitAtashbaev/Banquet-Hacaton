from django.urls import path
from .views import FavoriteView, FavoriteListView

urlpatterns = [
    path('favorite/<int:restaurant_id>/', FavoriteView.as_view(), name='favorite'),
    path('favorites/', FavoriteListView.as_view(), name='favorites'),
]