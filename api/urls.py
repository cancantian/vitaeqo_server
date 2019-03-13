from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('wechat_users/', views.WeChatUserListView.as_view(), name='wechat_user_list'),
	path('insert_user/', views.insert_user, name='insert_user'),
	path('query_by_openid/', views.query_by_openid, name='query_by_openid'),
]