from django.urls import path
from .views import CreateRestaurant, RetrieveUpdateDestroyRestaurant

urlpatterns = [
    path('create/', CreateRestaurant.as_view()),
    path('update/<int:pk>/', RetrieveUpdateDestroyRestaurant.as_view())
]
