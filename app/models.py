from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    street = models.TextField(default='', max_length=500, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    city = models.CharField(default='', max_length=40, blank=True)
    country = models.CharField(default='', max_length=40, blank=True)
    admin = models.BooleanField(default=False, blank=True)
    medium_rate = models.FloatField(null=True, blank=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Category(models.Model):
    parent_id = models.ForeignKey('Category', null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    id_seller = models.ForeignKey('auth.User')
    id_category = models.ForeignKey('Category')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date_of_sale = models.DateTimeField(
            default=timezone.now)
    starting_price = models.FloatField(null=True, blank=True)
    min_bid = models.FloatField(null=True, blank=True)
    current_price = models.FloatField(null=True, blank=True)
    immediate_price = models.FloatField(null=True, blank=True)
    end_date_of_sale = models.DateTimeField(
            default=timezone.now)
    purchased = models.BooleanField(default=False)
    medium_rate =  models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class RateUser(models.Model):
    id_rated_user = models.ForeignKey('auth.User', related_name='id_rated_user')
    id_rating_user = models.ForeignKey('auth.User', related_name='id_rating_user')
    rate = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return self.rate

class RateProduct(models.Model):
    id_product = models.ForeignKey('Product')
    rate = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.rate

class Bid(models.Model):
    id_product = models.ForeignKey('Product')
    id_user = models.ForeignKey('auth.User')
    bid_amount = models.FloatField()

    def __str__(self):
        return self.bid_amount