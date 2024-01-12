from . import views
from django.urls import path
urlpatterns = [
    path('menu', views.menu),
    path('item/<int:id>', views.item),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
]