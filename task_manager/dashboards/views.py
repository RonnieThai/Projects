from django.shortcuts import render, redirect 

from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Task, Category
from reporting.models import CompletedTask
from django.utils import timezone
import time
from .forms import CategoryForm, NewTaskForm

@login_required
def index(request):
    #Reverse Order
    todos= Task.objects.filter(complete=False, in_progress=False, user=request.user).order_by('-created_at')
    completed = Task.objects.filter(completed=True, user=request.user).order_by('-completed_at').filter(completed_at_get=timezone.now()
                                                                                                        .replace(hour=0, minute=0, second=0, microsecond=0))
    in_progress = Task.objects,filter(in_progress=True, user=request.user)
    categories = Category.objects.filter(user=request.user)
    
    context = {
        "task_todo": todos,
        "task_completed": completed,
        "task_in_progress": in_progress,
        "categories": categories,
        "task_form": NewTaskForm(),
        "category_form": CategoryForm()
    }
    return render(request, 'dashboard/tasks_list.html', context)

@login_required
def in_progress(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('dashboard:index')

@login_required
def undo_progress(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('dashboard:index')

@login_required
def completed(request, id):
    try:
        task = Task.objects.get(id=id, user=request.user)
        task.completed = not task.completed
        task.completed_at = timezone.now()
        task.in_progress = False
        task.save()
        if task.completed:
            CompleteTask.objects.create(
                title = task.title, 
                created_at=task.created_at, 
                completed_at=task.completed_at, 
                category=task.category.name if task.category else None, 
                user=task.user)
        return redirect('dashboard:index')
    
    except Task.DoesNotExist:
        return HttpResponseNotFound("Task not Found")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred while processing your request. Please try again in a few minutes.")
    