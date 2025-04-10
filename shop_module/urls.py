from django.urls import path
from .views import ProductListView, ProductDetailView, cart_view, cart_add_ajax_view, cart_remove_ajax_view

app_name = "shop"
urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("cart/", cart_view, name="cart"),
    path("cart/add/<product_id>", cart_add_ajax_view, name="cart-add"),
    path("cart/remove/<product_id>", cart_remove_ajax_view, name="cart-remove"),
]
