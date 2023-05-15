from django.contrib import admin
from .models import Restaurants, Favorite, Comment, Menu


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'price_people', 'locate', 'working_hours', 'features']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'date_added']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'restaurant', 'text', 'created_at', 'updated_at']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'description', 'image',]
