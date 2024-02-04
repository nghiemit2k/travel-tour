from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class Tours(models.Model):
    name_tour = models.CharField(max_length=10)
    price_adult = models.DecimalField(max_digits=10,decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='tours/%Y/%m', default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name_tour
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết với người dùng
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, related_query_name='booking')
    adults_count = models.PositiveIntegerField()
    children_count = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def calculate_total_price(self):
        return (self.adults_count * self.tour.price_adult) + (self.children_count * self.tour.price_child)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

#
class News(models.Model):
    name = models.CharField(max_length=10, unique=True)
    content = RichTextField()
    create_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Comment(Interaction):
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    comments = models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    content = RichTextField()

class Rating(Interaction):
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=False)
    rating = models.SmallIntegerField(default=0)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=False)
    class Meta:
        unique_together =('user','news')


