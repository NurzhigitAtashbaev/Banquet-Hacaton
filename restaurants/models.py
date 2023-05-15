from django.db import models

from applications.account.models import CustomUser


class Rating:
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

    ALL = (
        (one, '⭐️'),
        (two, '⭐⭐'),
        (three, '⭐⭐⭐'),
        (four, '⭐⭐⭐⭐'),
        (five, '⭐⭐⭐⭐⭐')
    )


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
    title = models.CharField(max_length=155, )
    # image = models.ImageField(upload_to='restaurant-image', )
    price_people = models.CharField(max_length=225)
    locate = models.CharField(max_length=200)
    working_hours = models.CharField(max_length=200)
    features = models.TextField(max_length=1000)

    def __str__(self):
        return "%s" % (self.title)


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='restaurant-image')

    def __str__(self):
        return "%s" % (self.restaurant.name)


class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(choices=Rating.ALL, null=True)

    class Meta:
        unique_together = ('restaurant', 'user',)

    def __str__(self):
        return f"Rating for {self.restaurant} by {self.user}: {self.stars}"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
