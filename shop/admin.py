from django.contrib import admin
from .models import Product, Message, Order, Order_items

# Model registration
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Order_items)
admin.site.register(Message)
