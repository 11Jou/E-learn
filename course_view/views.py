from django.shortcuts import render , redirect
from django.http import HttpResponse , HttpResponseNotFound , JsonResponse
from django.contrib.auth.decorators import login_required , user_passes_test
from register.models import Student , Instructor
from instructor.models import StudentCourseAccess , Course , Lesson , Section , Quiz , CompleteCourse , LiveMeeting
from student.models import QuizResult , Comment, Reply
from datetime import datetime
import pytz
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.core import serializers


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

@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def lesson_view(request, id):
    current_student = Student.objects.get(user=request.user)
    current_lesson = Lesson.objects.get(id=id)
    related_quiz = Quiz.objects.filter(lesson = current_lesson)
    passed_quiz_count = QuizResult.objects.filter(lesson = current_lesson, student = current_student, passed = "Passed").count()
    all_result = []
    for quiz in related_quiz:
        quiz_result = {}
        result_quiz = QuizResult.objects.filter(lesson = current_lesson, quiz = quiz, student = current_student).exists()
        if result_quiz:
            quiz_result[quiz] = QuizResult.objects.get(lesson = current_lesson, quiz = quiz, student = current_student)
        else:
            quiz_result[quiz] = 'Not Answerd'
        all_result.append(quiz_result)
    student_lesson = StudentCourseAccess.objects.get(student = current_student, lesson=current_lesson)
    if passed_quiz_count == related_quiz.count() and related_quiz.count() != 0:
        student_lesson.is_complete = True
    else:
        student_lesson.is_complete = False
    student_lesson.save()
    sections = Section.objects.filter(lesson=current_lesson)
    first_section = sections.first() 
    return render(request, 'lesson_details.html', {'lesson': current_lesson, 'sections': sections, 
                                                'default_section': first_section,
                                                'quizs_result':all_result,})


@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def section_view(request, id):
    current_student = Student.objects.get(user=request.user)
    current_section = Section.objects.get(id=id)
    online = LiveMeeting.objects.filter(section=current_section).first()
    if online:
        egypt_timezone = pytz.timezone('Africa/Cairo')
        online_start_time = timezone.localtime(online.start_time, timezone=egypt_timezone)
    comments = Comment.objects.filter(section=current_section)
    return render(request, 'section_template.html', {'section': current_section, 'online': online, 'comments': comments})


@login_required
def add_comment(request, id):
    #current_student = Student.objects.get(user = request.user)
    current_section = Section.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST.get('comment')
        new_comment = Comment(person=request.user, section=current_section, content=comment)
        new_comment.save()
        return JsonResponse({"comment": new_comment.content})
    
@login_required
def add_reply(request, id):
    comment_to_replay = Comment.objects.get(id=id)
    if request.method == "POST":
        reply = request.POST.get('reply')
        new_reply = Reply(comment = comment_to_replay, person = request.user, content = reply)
        new_reply.save()
        return JsonResponse({"reply": new_reply.content})
    

@login_required
def view_replies(request, id):
    comment = Comment.objects.get(id=id)
    all_replies = Reply.objects.filter(comment=comment)
    all_data = []
    for i in all_replies:
        data = {
            i.person.username : i.content
        }
        all_data.append(data)
    return JsonResponse({'replies':all_data})

@login_required
def pdf_view(request, pdfId):
    pdf_document = Section.objects.get(id=pdfId)
    fs = FileSystemStorage()
    pdf_path = str(pdf_document.pdf)

    if fs.exists(pdf_path):
        with fs.open(pdf_path) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
    else:
        return HttpResponseNotFound("Not Found")

