from django.db import models
from uuid import uuid4
from gyms.models import Gym


class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    gym = models.ForeignKey(to=Gym, on_delete=models.PROTECT, related_name="students")
    name = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class StudentStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    student = models.ForeignKey(to=Student, unique=True, on_delete=models.CASCADE, related_name="status")
    is_overdue = models.BooleanField(default=True)
    last_checked = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student}"
