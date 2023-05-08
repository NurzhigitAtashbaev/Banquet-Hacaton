from django.contrib import admin
from .models import Restaurant, Favorite, Category, RestaurantImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Restaurant)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'price_people', 'locate', 'working_hours', 'features']


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'image']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'date_added']

