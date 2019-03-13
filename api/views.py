import json
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.list import ListView
from .models import WeChatUser
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, reverse

def index(request):
	return HttpResponse("Hello, world. You're at the api index.")

class WeChatUserListView(ListView):

	model = WeChatUser
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context

@csrf_exempt
def insert_user(request):
	try:
		openid = request.POST.get('openid')
		WeChatUser.objects.get(openid=openid)
		return HttpResponse(status=201)
	except ObjectDoesNotExist:
		nickname = request.POST.get('nickname')
		avatarUrl = request.POST.get('avatarUrl')
		WeChatUser.create(openid=openid, nickName=nickname, avatarUrl=avatarUrl)
		return HttpResponse(status=201)
	except:
		return HttpResponse(status=400)

@csrf_exempt
def query_by_openid(request):
	try:
		openid = request.POST.get('openid')
		wx_user = WeChatUser.objects.filter(openid=openid)
		wx_user = get_object_or_404(wx_user)
	except:
		return HttpResponse(status=400)
	else:
		data = {'nickName': wx_user.nickName, 'avatarUrl': wx_user.avatarUrl}
		return HttpResponse(json.dumps(data), status=201)