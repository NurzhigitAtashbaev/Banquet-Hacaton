from django.db import models
from applications.account.models import CustomUser

from applications.account.models import CustomUser


class Restaurants(models.Model):
    title = models.CharField(max_length=155, )
    image = models.ImageField(upload_to='restaurant-image', )
    price_people = models.CharField(max_length=225)
    locate = models.CharField(max_length=200)
    working_hours = models.CharField(max_length=200)
    features = models.TextField(max_length=1000)

    # comment = models.ForeignKey('Comment', on_delete=models.CASCADE)


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.owner.email} - {self.restaurant.title}'