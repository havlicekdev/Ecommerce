import datetime
from django.db import models
from users.models import User


# products
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=300)

    def __str__(self):
        return self.title


# order
ORDER_STATUS = (
    ("PR", "Přijato"),
    ("ZA", "Zaplaceno"),
    ("OD", "Odesláno"),
    ("FA", "Fakturováno"),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, default=1)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PR')


# order items
class Order_items(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    product_title = models.CharField(max_length=200)
    product_price = models.IntegerField()
    product_quantity = models.IntegerField()
    product_item_price = models.IntegerField()
    product_category = models.CharField(max_length=200)
    product_description = models.CharField(max_length=200)


# contact form messages (copy of sent email)
class Message(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
