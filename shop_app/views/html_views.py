from django.shortcuts import render
import uuid
import os
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from shop_app.models import Product
from shop_app.forms import ProductForm
from shop_app.helper import handle_uploaded_file


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


def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_prod = form.save(commit=False)
            filename = str(uuid.uuid4())
            filepath = os.path.join(settings.IMG_ROOT, filename)
            rel_filepath = os.path.join(settings.MEDIA_URL, filename)
            handle_uploaded_file(request.FILES['img'], filepath)
            new_prod.img = rel_filepath
            new_prod.save()
            return redirect('shop_app:product_list')
    else:
        form = ProductForm()
    return render(request, 'shop_app/product_form.html', {'form': form})


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'shop_app/product_delete.html'
    success_url = reverse_lazy('shop_app:product_list')


class UpdateProduct(UpdateView):
    model = Product
    fields = ['name','price', 'available']
    template_name = 'shop_app/product_update.html'
    success_url = reverse_lazy('shop_app:product_list')
