from django.contrib import admin
from .models import Restaurants, Favorite


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'price_people', 'locate', 'working_hours', 'features']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ['user', 'restaurant']
=======
    list_display = ['user', 'item', 'date_added']
>>>>>>> 9a9fa62a42a18720db69b9c8a7b46646c83b495a
