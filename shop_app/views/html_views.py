from django.shortcuts import render
import uuid
import os
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from shop_app.models import Product, Order
from shop_app.forms import ProductForm
from shop_app.helper import handle_uploaded_file
from utils.tx_cloud.bucket import TXBucket


@staff_member_required
def dashboard(request):
    return render(request, 'shop_app/dashboard.html', {'user': request.user})


@staff_member_required
def product_list(request):
    prod_list = Product.objects.order_by('-id').all()
    paginator = Paginator(prod_list, 5)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'shop_app/product_list.html', {'products': products})


@staff_member_required
def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_prod = form.save(commit=False)
            filename = str(uuid.uuid4())
            txb = TXBucket()
            url = txb.upload_img(fp=request.FILES['img'], bucket_file_name=filename)
            new_prod.img = url
            new_prod.save()
            return redirect('shop_app:product_list')
    else:
        form = ProductForm()
    return render(request, 'shop_app/product_form.html', {'form': form})


@staff_member_required
def order_list(request):
    all_orders = Order.objects.order_by('-id').all()
    paginator = Paginator(all_orders, 5)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return render(request, 'shop_app/order_list.html', {'orders': orders})


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_staff'
    model = Product
    template_name = 'shop_app/product_delete.html'
    success_url = reverse_lazy('shop_app:product_list')


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    model = Product
    fields = ['name','price', 'available']
    template_name = 'shop_app/product_update.html'
    success_url = reverse_lazy('shop_app:product_list')
