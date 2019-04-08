"""wechatapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from user_app import views as user_app_Views

router = routers.DefaultRouter()
router.register(r'users', user_app_Views.UserViewSet)
router.register(r'groups', user_app_Views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user_app/', include('user_app.urls')),
    path('shop/', include('shop_app.urls')),
    path('test/', include(router.urls)),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
