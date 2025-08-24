from django.contrib import admin
from .models import Student, StudentStatus


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "reference",]


@admin.register(StudentStatus)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["student", "is_overdue", "last_checked",]