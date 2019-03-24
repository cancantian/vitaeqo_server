import json
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic.list import ListView
from .models import WeChatUser
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .constants import *
import requests
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


def index(request):
	return HttpResponse("Hello, world. You're at the api index.")

class WeChatUserListView(ListView):

	model = WeChatUser
	paginate_by = 100  # if pagination is desired

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context

@api_view(['GET'])
def insert_user(request):
	try:
		code = request.GET.get('code')
		wx_auth_url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(WX_APPID, WX_APP_SECRET, code)
		r = requests.get(wx_auth_url)
		r_body = json.loads(r.text)
		openid = r_body['openid']
		r_session = r_body['session_key']
		# WeChatUser.objects.get(openid=openid)
		user = User.objects.get(username=openid)
		token = RefreshToken.for_user(user)
		auth_token = str(token.access_token)
		data = {'dj_uid': user.id, 'auth_token': auth_token}
		return JsonResponse(data, safe=False)
	except ObjectDoesNotExist:
		user = User.objects.create_user(username=openid, password=settings.SECRET_KEY)
		user.save()
		token = RefreshToken.for_user(user)
		auth_token = str(token.access_token)
		data = {'dj_uid': user.id, 'auth_token': auth_token}
		return JsonResponse(data, safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_info(request):
	try:
		openid = request.user.username
		wx_user = WeChatUser.objects.filter(openid=openid)
		wx_user = get_object_or_404(wx_user)
	except:
		return HttpResponse(status=400)
	else:
		data = {'nickName': wx_user.nickName, 'avatarUrl': wx_user.avatarUrl}
		return HttpResponse(json.dumps(data), status=201)

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer