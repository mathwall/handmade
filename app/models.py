from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='avatars', null=True, blank=True)    
    description = models.TextField(null=True, blank=True)
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
    photo = models.ImageField(upload_to='blog', null=True, blank=True)
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
    parent = models.ForeignKey('Category', null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey('auth.User', related_name='seller')
    buyer = models.ForeignKey('auth.User', related_name='buyer', null=True, blank=True)
    category = models.ForeignKey('Category')
    photo = models.ImageField(upload_to='products', null=True, blank=True)    
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date_of_sale = models.DateField(null=False, blank=False)
    end_date_of_sale = models.DateField(null=False, blank=False)
    starting_price = models.FloatField(null=True, blank=True)
    min_bid = models.FloatField(null=True, blank=True)
    immediate_price = models.FloatField(null=True, blank=True)
    current_price = models.FloatField(null=True, blank=True)
    purchased = models.BooleanField(default=False)
    avg_rate = models.FloatField(null=True, blank=True)
    nb_rate = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class RateUser(models.Model):
    rated_user = models.ForeignKey('auth.User', related_name='id_rated_user')
    rating_user = models.ForeignKey('auth.User', related_name='id_rating_user')
    rate = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return self.pk


class RateProduct(models.Model):
    product = models.ForeignKey('Product')
    rating_user = models.ForeignKey('auth.User', null=True)    
    rate = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.product.title + str(self.rate)


# Update the rate avg of the product each time a new rateProduct is created or updated
@receiver(post_save, sender=RateProduct)
def update_rate_product(sender, instance, created, **kwargs):
    product = instance.product
    avg = RateProduct.objects.filter(product=product).aggregate(Avg('rate'))
    nb_rate = RateProduct.objects.filter(product=product).count()
    product.avg_rate = avg['rate__avg']
    product.nb_rate = nb_rate
    product.save()


class Bid(models.Model):
    product = models.ForeignKey('Product')
    user = models.ForeignKey('auth.User')
    bid_amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        desc = str(self.product) + '/' + str(self.user) + '/' + str(self.bid_amount)
        return desc 