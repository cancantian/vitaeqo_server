from django.db import models

# Create your models here.

class WeChatUser(models.Model):
	openid = models.CharField(max_length=200, unique=True)
	nickName = models.CharField(max_length=200)
	avatarUrl = models.CharField(max_length=200)

	@classmethod
	def create(cls, openid, nickName, avatarUrl):
		wc_user = cls(openid=openid, nickName=nickName, avatarUrl=avatarUrl)
		wc_user.save()
		return wc_user