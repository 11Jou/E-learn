from django.shortcuts import render 
from django.contrib.auth.decorators import login_required , user_passes_test
from register.models import Student , Instructor
from instructor.models import StudentCourseAccess , Course , Lesson ,  CompleteCourse
from datetime import datetime
from django.utils import timezone



@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def student_course(request):
    current_student = Student.objects.get(user=request.user)
    related_instructor = Instructor.objects.get(id=current_student.invited_by.id)
    courses_data = []
    related_course = Course.objects.filter(instructor = related_instructor)
    for course in related_course:
        check_complete = CompleteCourse.objects.filter(student=current_student, course=course)
        if check_complete:
            course_info = {'course':course, 'completed':True}
        else:
            course_info = {'course':course, 'completed':False}
        courses_data.append(course_info)
    return render(request, 'student_course.html', {'student':current_student , 
                                                'instructor':related_instructor,
                                                'courses':courses_data})

@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def course_details(request, id):
    current_student = Student.objects.get(user=request.user)
    current_course = Course.objects.get(id=id)
    lessons = Lesson.objects.filter(course = current_course)
    lesson_data = []
    finished_lessons = 0
    for lesson in lessons:
        student_access = StudentCourseAccess.objects.get(student=current_student, lesson=lesson.id)
        if student_access.is_complete:
            finished_lessons += 1
        current_time = datetime.now()
        current_time_str = f"{current_time}"
        current_time = timezone.make_aware(datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S.%f"))
        if student_access.specific_time_start <= current_time <= student_access.specific_time_end:
            can_access = True
        else:
            can_access = False
        lesson_info = {'lesson':lesson, 'can_view_anytime':student_access.can_view_anytime, 'can_access':can_access
                    ,'completed': student_access.is_complete}
        lesson_data.append(lesson_info)
    if finished_lessons == lessons.count() and lessons.count() != 0:
        if CompleteCourse.objects.filter(student = current_student, course = current_course).exists() == False:
            newComplete = CompleteCourse(student = current_student, course = current_course)
            newComplete.save()
    elif CompleteCourse.objects.filter(student = current_student, course = current_course).exists():
        deleteRecord = CompleteCourse.objects.get(student = current_student, course = current_course)
        deleteRecord.delete()
    return render(request, 'course_lessons.html', {'course':current_course, 'lessons':lesson_data})