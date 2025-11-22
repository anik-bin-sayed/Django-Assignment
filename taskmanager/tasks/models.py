from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending' )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.description} "
    
    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return date.today() > self.due_date
        return False