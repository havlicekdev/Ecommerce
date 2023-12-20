from rest_framework import serializers
from shop.models import Product


# product serializer
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category', 'description', 'image']
