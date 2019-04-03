from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('wechat_users/', views.WeChatUserListView.as_view(), name='wechat_user_list'),
	path('insert_user/', views.insert_user, name='insert_user'),
	path('get_user_info/', views.get_user_info, name='get_user_info'),
]