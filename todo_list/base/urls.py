from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path('', TaskList.as_view(), name='tasklist'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task/create-new/', TaskCreate.as_view(), name='taskcreate'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='taskupdate'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='taskdelete'),
]