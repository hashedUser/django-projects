from django.shortcuts import render
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

# View for listing tasks
class TaskList(ListView):
    model = Task
    template_name = "base/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10
    ordering = ['-created']

# View for displaying details of a task
class TaskDetail(DetailView):
    model = Task
    template_name = 'base/task.html'
    context_object_name = "task"

# View for creating a new task
class TaskCreate(CreateView):
    model = Task
    template_name = 'base/create_new_task.html'
    fields = "__all__"
    success_url = reverse_lazy('tasklist')


class TaskUpdate(UpdateView):
    model = Task
    template_name = 'base/update_task.html'
    fields = "__all__"
    success_url = reverse_lazy('tasklist')
    

class TaskDelete(DeleteView):
    model = Task
    template_name = 'base/delete_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasklist')
