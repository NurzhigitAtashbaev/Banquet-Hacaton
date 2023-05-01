from django.contrib import admin
from .models import Restaurant, Favorite


<<<<<<< HEAD
@admin.register(Restaurant)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price_people', 'locate', 'working_hours', 'features']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'date_added']
=======
@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price_people', 'locate', 'working_hours', 'features']
>>>>>>> master
