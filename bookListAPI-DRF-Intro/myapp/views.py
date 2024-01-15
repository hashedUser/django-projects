from .models import Menu, Category
from .serializers import MenuSerializer, CategorySerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import api_view, renderer_classes, permission_classes, throttle_classes


from django.contrib.auth.models import User, Group
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
    

# Throttling for anonymous user
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(response):
    return Response({"message":"successful"})


# Throttling for authenticated user
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only!"})


# Assign a particular user to managers group
@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data.get['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'GET':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            
        return Response({"message":"ok"})
    
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)