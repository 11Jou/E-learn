from django.contrib.auth.decorators import login_required , user_passes_test
from django.shortcuts import render , redirect
from instructor.forms import *
from register.models import Instructor , Student
from instructor.models import *


# View Course of logged in instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def course_view(request):
    current_instructor = Instructor.objects.get(staffuser = request.user)
    courses = Course.objects.filter(instructor = current_instructor)
    return render(request , 'instructor_course.html', {'courses':courses})

# Delete Course from instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('instructor_courses')


# Upload course by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def upload_course(request):
    form = CourseForm()
    instructor = Instructor.objects.get(staffuser = request.user)
    if request.method == "POST":
        form = CourseForm(request.POST ,  request.FILES)
        if form.is_valid():
            course_name = form.cleaned_data['courseName']
            course_image = form.cleaned_data['courseImage']
            desc = form.cleaned_data['Desc']
            course_type = form.cleaned_data['courseType']
            newCourse = Course(instructor = instructor, courseName = course_name, image = course_image
                            , description = desc, Type = course_type)
            newCourse.save()
            return redirect('upload_lesson', id=newCourse.id)
        else:
            return render(request , 'upload_course.html', {'form':form})
    return render(request , 'upload_course.html', {'form':form})