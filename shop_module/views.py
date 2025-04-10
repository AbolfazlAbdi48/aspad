import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from extentions.cart import Cart
from shop_module.models import Product


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"


def cart_view(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }
    return render(request, 'shop/cart.html', context)


def cart_add_ajax_view(request, product_id):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            cd = data.get('payload')  # cleaned daya
            count = cd.get('count')
            # check count greater than 1
            if int(count) < 1:
                count = 1

            cart = Cart(request)
            product = get_object_or_404(Product, pk=product_id)

            # check for product stock
            if int(count) <= product.stock:
                cart.add(product, count=1, override_count=True)
                return JsonResponse({'status': 'added'})
            return JsonResponse({'status': 'failed'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')


def cart_remove_ajax_view(request, product_id):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'DELETE':
            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id)

            cart.remove(product)
            return JsonResponse({'status': 'deleted', 'total_price': cart.get_total_price()})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')
