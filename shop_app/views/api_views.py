from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic.list import ListView
from shop_app.models import Product
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from shop_app.serializers import ProductSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for listing or retrieving Products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
