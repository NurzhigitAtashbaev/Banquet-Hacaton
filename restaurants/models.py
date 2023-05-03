from django.db import models
from applications.account.models import CustomUser

CATEGORY_CHOICES = (
    ('Внутри города', 'Внутри города'),
    ('За городом', 'За городом')
)


class Category(models.Model):
    name = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default=None)

    def __str__(self):
        return str(self.name)


class Restaurant(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=155, )
    image = models.ImageField(upload_to='restaurant-image', )
    price_people = models.CharField(max_length=225)
    locate = models.CharField(max_length=200)
    working_hours = models.CharField(max_length=200)
    features = models.TextField(max_length=1000)


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


