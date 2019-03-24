from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class WeChatUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	openid = models.CharField(max_length=200, unique=True)
	nickName = models.CharField(max_length=200)
	avatarUrl = models.CharField(max_length=200)

	@classmethod
	def create(cls, openid, nickName, avatarUrl):
		wc_user = cls(openid=openid, nickName=nickName, avatarUrl=avatarUrl)
		wc_user.save()
		return wc_user

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			WeChatUser.objects.create(user=instance, openid=instance.username)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.wechatuser.save()