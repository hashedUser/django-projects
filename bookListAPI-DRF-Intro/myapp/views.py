from .models import Menu, Category
from .serializers import MenuSerializer, CategorySerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes


from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
@api_view(['GET', 'POST'])
def menu(request):
    if request.method == 'GET':
        menu = Menu.objects.select_related('category').all()

        # Query Params
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

        # Filter and Search
        if category_name:
            menu = menu.filter(category__title=category_name)

        if to_price:
            menu = menu.filter(price=to_price)

        if search:
            menu = menu.filter(title__icontains=search)

        if ordering:
            ordering_fields = ordering.split(",")
            menu = menu.order_by(*ordering_fields)

        # Pagination
        paginator = Paginator(menu, per_page=perpage)
        try:
            menu = paginator.page(number=page)
        except EmptyPage:
            menu = []


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

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})


# Working with user groups
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only Manager can see this"})
    else:
        return Response({"message":"You are not authorized"}, 403)