from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price_people', 'locate', 'working_hours', 'features']


