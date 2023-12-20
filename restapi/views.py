from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from shop.models import Product


# get all the products: only GET allowed
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']


# get only products from particular category: only GET allowed
class SportsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category='Sports')
    serializer_class = ProductSerializer
    http_method_names = ['get']


# get only products from particular category: only GET allowed
class ElectronicsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category='Electronics')
    serializer_class = ProductSerializer
    http_method_names = ['get']
