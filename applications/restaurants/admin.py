from django.contrib import admin
from .models import Restaurants, Favorite, Comment, Menu, RestaurantImage


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_people', 'locate', 'working_hours', 'features']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'items', 'date_added']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'restaurant', 'text', 'created_at', 'updated_at']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'description', 'image',]

@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'image']