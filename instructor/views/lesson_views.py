from django.contrib.auth.decorators import login_required , user_passes_test
from django.shortcuts import render, redirect
from instructor.forms import *
from register.models import Instructor , Student
from instructor.models import *
from django.core.paginator import Paginator
from datetime import datetime



# Upload lesson by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def upload_lesson(request, id):
    form = LessonForm()
    current_instructor = Instructor.objects.get(staffuser = request.user)
    students = Student.objects.filter(invited_by = current_instructor)
    student_ids = students.values_list('id', flat=True)
    course = Course.objects.get(id=id)
    lesson = Lesson.objects.filter(course = course)
    if request.method == "POST":
        if "lesson-form" in request.POST:
            form = LessonForm(request.POST , request.FILES)
            if form.is_valid():
                lesson_name = form.cleaned_data['lessonName']
                content = form.cleaned_data['content']
                newLesson = Lesson(course=course, name = lesson_name, content=content)
                newLesson.save()
                for i in student_ids:
                    student = Student.objects.get(id=i)
                    newAccess = StudentCourseAccess(student = student, lesson=newLesson)
                    newAccess.save()
                completed_course = CompleteCourse.objects.filter(course = course)
                for i in completed_course:
                    i.delete()
                return redirect('upload_lesson', id=id)
            else:
                return render(request , 'lessons.html', {'form':form, 'course':course, 'lessons':lesson, 'students':students})
        elif "student-form" in request.POST:
            selected_student = request.POST.getlist('students')
            if selected_student:
                selected_lesson = request.POST.get('lessons')
                if 'anytime' not in request.POST:
                    start_date = request.POST.get("start_date")
                    end_date = request.POST.get("end_date")
                    start_time = request.POST.get("start_time")+':00'
                    end_time = request.POST.get("end_time")+':00'
                    start_datetime_str = f"{start_date} {start_time}" ; end_datetime_str = f"{end_date} {end_time}"
                    start_datetime = timezone.make_aware(datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S"))
                    end_datetime = timezone.make_aware(datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S"))
                    can_view_anytime = False
                else:
                    start_datetime = timezone.now()
                    end_datetime = timezone.now()
                    can_view_anytime = True
                for i in selected_student:
                    student = Student.objects.get(id=i)
                    existing_access = StudentCourseAccess.objects.filter(student=student, lesson=selected_lesson).first()
                    existing_access.specific_time_start = start_datetime
                    existing_access.specific_time_end = end_datetime
                    existing_access.can_view_anytime = can_view_anytime
                    existing_access.save()
            return redirect('upload_lesson', id=id)        
    return render(request , 'lessons.html', {'form':form, 'course':course, 'lessons':lesson, 'students':students})



# Delete lesson by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def delete_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    courseId = lesson.course.id
    lesson.delete()
    return redirect('upload_lesson' ,id=courseId)



# Edit lesson by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def edit_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    courseId = lesson.course.id
    if request.method == "POST":
        lesson.name = request.POST.get('lesson_name')
        lesson.content = request.POST.get('lesson_content')
        lesson.save()
        return redirect('upload_lesson' ,id=courseId)
    return render(request, 'edit_lesson.html', {'lesson':lesson})