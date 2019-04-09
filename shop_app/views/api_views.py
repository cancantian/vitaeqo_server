from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic.list import ListView
from shop_app.models import Product, OrderItem, Order
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from shop_app.serializers import ProductSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for listing or retrieving Products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderItemViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """
        A ViewSet for create, list, retrieve, update OrderItem.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
        A ViewSet for create, list, retrieve, update Order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
