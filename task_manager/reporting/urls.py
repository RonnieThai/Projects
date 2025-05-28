from django.urls import path
from . import views 

app_name = 'reporting'

urlpatterns = [
    path('history/', views.task_history, name='history'),
    path('clear_history5364/', views.clear_history, name='clear_history'),
]
