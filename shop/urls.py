from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Root.as_view(), name="root"),
    path("home/", views.index, name="index"),
    path("search/", views.Search.as_view(), name="search"),
    path("<int:id>/product-detail/", views.detail, name="detail"),
    path("products/", views.products, name="products"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("cart/", views.cart, name="cart"),
    path("cart/add", views.cart_add, name="cart_add"),
    path("cart/dec", views.cart_dec, name="cart_dec"),
    path("cart/delete", views.cart_delete, name="cart_delete"),
    path("cart/remove-item", views.cart_remove_item, name="cart_remove_item"),
    path("checkout/", views.checkout, name="checkout"),
]