from django.shortcuts import render
from django.views.generic import ListView, DetailView

from shop_module.models import Product


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
