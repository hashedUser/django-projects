from .models import Menu, Category
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import MenuSerializer, CategorySerializer
from rest_framework.decorators import api_view, renderer_classes


# Create your views here.
@api_view(['GET', 'POST'])
def menu(request):
    if request.method == 'GET':
        menu = Menu.objects.select_related('category').all()
        serialized_menu = MenuSerializer(menu, many=True, context={'request':request})
        return Response(serialized_menu.data)
    if request.method == 'POST':
        # Deserialize the request data
        serialized_menu = MenuSerializer(data=request.data)
        serialized_menu.is_valid(raise_exception=True)
        serialized_menu.save()
        return Response(serialized_menu.data, status.HTTP_201_CREATED)


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

# Trying out renderers which are not included in the default. (Default are JSONRenderer and HTMLRenderer)
@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu_items(request):
    items = Menu.objects.select_related('category').all()
    ser_item = MenuSerializer(items, many=True)
    return Response({'data':ser_item.data}, template_name='menu-items.html')
