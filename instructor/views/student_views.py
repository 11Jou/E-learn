from django.contrib.auth.decorators import login_required , user_passes_test
from django.shortcuts import render, redirect
from instructor.forms import *
from register.models import Instructor , Student
from instructor.models import *
from django.core.paginator import Paginator


# View instructor's students
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def student_view(request):
    current_instructor = Instructor.objects.get(staffuser = request.user)
    students = Student.objects.filter(invited_by = current_instructor).order_by('name')
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request , 'all_student.html', {'students':students})


@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def delete_student(request, id):
    deleted_student = User.objects.get(id=id)
    deleted_student.delete()
    return redirect('instructor_student')