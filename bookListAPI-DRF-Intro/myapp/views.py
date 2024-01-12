from .models import Menu, Category
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404
from .serializers import MenuSerializer, CategorySerializer


# Create your views here.
@api_view()
def menu(request):
    menu = Menu.objects.select_related('category').all()
    serialized_menu = MenuSerializer(menu, many=True, context={'request':request})
    return Response(serialized_menu.data)


@api_view(['GET', 'POST'])
def item(request, id):
    item = get_object_or_404(Menu, pk=id)
    serialized_item = MenuSerializer(item)
    return Response(serialized_item.data)    
    

@api_view()
def category_detail(request,pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)