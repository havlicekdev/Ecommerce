from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.user, name="user"),
    path("register", views.register, name="user_register"),

]
