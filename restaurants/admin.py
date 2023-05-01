from django.contrib import admin
from .models import Restaurants, Favorite


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'price_people', 'locate', 'working_hours', 'features']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'date_added']
