from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'shop_app'
urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^product/new$', views.new_product, name='new_product'),
    url(r'^product/delete/(?P<pk>\d+)/$', views.DeleteProduct.as_view(), name='delete_product'),
	url(r'^product/(?P<pk>\d+)/update/$', views.UpdateProduct.as_view(), name='update_product'),
]