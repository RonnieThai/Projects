from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import CompletedTask
from django.utils import  timezone

@login_required
def task_history(request):
    completed = CompletedTask.objects.filter(user=request.user).order_by('-completed-at')
    context = {
        "page": completed,
    }
    return render(request, 'reporting/task_history.html', context)

@staff_member_required
def clear_history(request):
    CompletedTask.objects.all().delete()
    return redirect('reporting:task_history')