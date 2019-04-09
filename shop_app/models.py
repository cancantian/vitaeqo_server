from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum
# Create your models here.


class Order(models.Model):
	ORDER_STATUS = (
		('New', 'New'),
		('Paid', 'Paid'),
		('Shipping', 'Shipping'),
		('Shipped', 'Shipped'),
		('Closed', 'Closed'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=ORDER_STATUS, default='New',)

	@receiver(post_save, sender=User)
	def create_order(sender, instance, created, **kwargs):
		if created:
			Order.objects.create(user=instance, status='New')


class Product(models.Model):
	name = models.CharField(max_length=200, null=False)
	price = models.FloatField(null=False)
	available = models.BooleanField(default=False)
	img = models.CharField(max_length=200, null=False)

	@receiver(models.signals.post_delete)
	def delete_img(sender, instance, *args, **kwargs):
		""" Deletes img files on `post_delete` """
		if instance.img:
			all_imgs = os.listdir(settings.MEDIA_ROOT)
			img_filename = next(fn for fn in all_imgs if fn in instance.img)
			img_abs_path = os.path.join(settings.MEDIA_ROOT, img_filename)
			os.remove(img_abs_path)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	count = models.PositiveIntegerField()


