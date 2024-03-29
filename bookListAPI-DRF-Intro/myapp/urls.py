from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu', views.menu),
    path('secret/', views.secret),
    path('item/<int:id>', views.item),
    path('menu_items', views.menu_items),
    path('token-auth/', obtain_auth_token),
    path('manager-view', views.manager_view),
    path('throttle-check', views.throttle_check),
    path('groups/manager/users', views.managers),
    path('throttle-check-auth', views.throttle_check_auth),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
]