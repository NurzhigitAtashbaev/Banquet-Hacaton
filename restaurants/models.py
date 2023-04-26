from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=155, )
    image = models.ImageField(upload_to='restaurant-image', )
    price_people = models.CharField(max_length=225)
    locate = models.URLField()
    working_hours = models.CharField(max_length=200)
    features = models.TextField(max_length=1000)

