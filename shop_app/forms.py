from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    img = forms.FileField()

    class Meta:
        model = Product
        fields = ['name', 'price', 'available', 'img']
