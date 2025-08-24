from django.db.models import signals
from django.dispatch import receiver
from .models import Student, StudentStatus


@receiver(signal=signals.post_save, sender=Student)
def create_student_status(sender, instance, created, **kwargs):
    if created:
        StudentStatus.objects.create(student=instance)