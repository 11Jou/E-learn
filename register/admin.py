from django.contrib import admin
from .models import Student , Instructor , Invitation

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Invitation)