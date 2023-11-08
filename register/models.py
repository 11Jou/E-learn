from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class Instructor(models.Model):
    staffuser = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{str(self.staffuser)} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.staffuser.is_staff or self.staffuser.is_superuser:
            raise ValueError("Only staff users can be instructors.")
        super().save(*args, **kwargs)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='student_photo/%Y/%m/%d/')
    invited_by = models.ForeignKey(Instructor, on_delete=models.CASCADE , to_field='id')

    def __str__(self):
        return f"{str(self.user)}"
    
    def save(self, *args, **kwargs):
        if self.user.is_superuser or self.user.is_staff:
            raise ValueError("Superusers or Staff users cannot be students.")
        super().save(*args, **kwargs)


class Invitation(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    staffuser = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    expiration_datetime = models.DateTimeField(blank=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return self.expiration_datetime <= timezone.now()
    

class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    related_instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{str(self.user)}"
