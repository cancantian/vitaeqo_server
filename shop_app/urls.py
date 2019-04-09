from django.conf.urls import url, include
from rest_framework import routers
from .views import html_views, api_views
app_name = 'shop_app'
router = routers.DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'order_items', api_views.OrderItemViewSet)
router.register(r'orders', api_views.OrderViewSet)
urlpatterns = [
    url(r'^$', html_views.dashboard, name='dashboard'),
    url(r'^products/$', html_views.product_list, name='product_list'),
    url(r'^api/', include(router.urls)),
    url(r'^product/new$', html_views.new_product, name='new_product'),
    url(r'^product/delete/(?P<pk>\d+)/$', html_views.DeleteProduct.as_view(), name='delete_product'),
    url(r'^product/(?P<pk>\d+)/update/$', html_views.UpdateProduct.as_view(), name='update_product'),
]