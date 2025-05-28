from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Task, Category
from reporting.models import CompletedTask
from django.utils import timezone
from .forms import CategoryForm, NewTaskForm


@login_required
def index(request):
    todos = Task.objects.filter(completed=False, inprogress=False, user=request.user).order_by('-created_at')
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    completed = Task.objects.filter(
        completed=True,
        user=request.user,
        completed_at__gte=today_start
    ).order_by('-completed_at')
    in_progress = Task.objects.filter(inprogress=True, user=request.user)
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
    task.inprogress = not task.inprogress
    task.save()
    return redirect('dashboard:index')


@login_required
def undo_progress(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.inprogress = not task.inprogress
    task.save()
    return redirect('dashboard:index')


@login_required
def completed(request, id):
    try:
        task = Task.objects.get(id=id, user=request.user)
        task.completed = not task.completed
        task.completed_at = timezone.now()
        task.inprogress = False
        task.save()

        if task.completed:
            CompletedTask.objects.create(
                title=task.title,
                created_at=task.created_at,
                completed_at=task.completed_at,
                category=task.category.name if task.category else None,
                user=task.user
            )

        return redirect('dashboard:index')

    except Task.DoesNotExist:
        return HttpResponseNotFound("Task not Found")

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred while processing your request. Please try again in a few minutes.")


@login_required
def create(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.completed = False
            task.user = request.user
            task.save()
            return redirect('dashboard:index')
    return redirect('dashboard:index')


@login_required
def update(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard:index')


@login_required
def delete(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('dashboard:index')


@login_required
def reset_all(request):
    Task.objects.filter(user=request.user).delete()
    return redirect('dashboard:index')


@login_required
def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
        return redirect('dashboard:index')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/create_category.html', {'category_form': form})


@staff_member_required
def clear_categories(request):
    Category.objects.all().delete()
    return redirect('dashboard:index')
