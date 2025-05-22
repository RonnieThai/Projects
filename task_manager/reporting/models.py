from django.db import models
from django.contrib.auth.models import User
from dashboards.models import Category

class CompleteTask(models.Model):
    title = models.CharField(max_length=255, default="Task")
    created_at = models.DateTimeField(null=True, blank=True)
    complete_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=255, default="Others")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Complete Task"