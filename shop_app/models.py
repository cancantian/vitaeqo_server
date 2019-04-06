from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum
# Create your models here.


class Status(Enum):
    Paid = "Paid"
    Shipping = "Shipping"
    Shipped = "Shipped"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')

    @classmethod
    def create(cls):
        cart = cls()
        cart.save()
        return cart

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Cart.objects.create(user=instance, openid=instance.username)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.cart.save()


class History(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    status = models.CharField(
      max_length=10,
      choices=[(Status, Status.value) for Status in Status]
    )


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    price = models.FloatField(null=False)
    available = models.BooleanField(default=False)
    img = models.CharField(max_length=200, null=False)
