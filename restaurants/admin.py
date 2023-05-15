from django.contrib import admin
from .models import Restaurant, RestaurantImage, Favorite, Rating, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'user', 'stars']


@admin.register(Restaurant)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'price_people', 'locate', 'working_hours', 'features']


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'image']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'date_added']
