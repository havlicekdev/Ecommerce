from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.RootView.as_view(), name="root"),
    path("home/", views.IndexView.as_view(), name="index"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<int:id>/product-detail/", views.DetailView.as_view(), name="detail"),
    path("products/", views.ProductsView.as_view(), name="products"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add", views.CartAddAjax.as_view(), name="cart_add"),
    path("cart/dec", views.CartDecAjax.as_view(), name="cart_dec"),
    path("cart/delete", views.CartDeleteAjax.as_view(), name="cart_delete"),
    path("cart/remove-item", views.CartRemoveItemView.as_view(), name="cart_remove_item"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
]