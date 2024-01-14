from .models import Menu, Category
from decimal import Decimal
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculateTax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    # category  = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name='category-detail'
    # )


    def calculateTax(self, product:Menu):
        return float(f"{product.price * Decimal(1.1):.2f}")


    def validate(self, attrs):
        if attrs['price'] < 2:
            raise serializers.ValidationError("Price should not be less than 2.0")
        
        if attrs['inventory'] < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        
        return super().validate(attrs)

    class Meta:
        model = Menu
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
    