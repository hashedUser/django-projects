from django.urls import path

from photos import views

urlpatterns = [
    path('', views.gallery, name="gallery"),
    path('add/', views.addPhoto, name="add"),
    path('photo/<str:pk>/', views.viewPhoto, name="photo"),
]