from django.contrib import admin
from .models import Restaurants


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price_people', 'locate', 'working_hours', 'features']
