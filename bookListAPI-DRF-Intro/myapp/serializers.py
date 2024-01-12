from .models import Menu, Category
from decimal import Decimal
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculateTax')
    # category  = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name='category-detail'
    # )
    def calculateTax(self, product:Menu):
        return float(f"{product.price * Decimal(1.1):.2f}")

    class Meta:
        model = Menu
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']