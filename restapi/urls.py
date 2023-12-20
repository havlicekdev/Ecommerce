from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, SportsViewSet, ElectronicsViewSet

# simple router for ViewSet
router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'sports', SportsViewSet)
router.register(r'electronics', ElectronicsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

