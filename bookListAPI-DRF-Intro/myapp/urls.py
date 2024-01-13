from . import views
from django.urls import path
urlpatterns = [
    path('menu', views.menu),
    path('menu_items', views.menu_items),
    path('item/<int:id>', views.item),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
]