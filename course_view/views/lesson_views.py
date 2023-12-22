from django.shortcuts import render 
from django.http import HttpResponse , HttpResponseNotFound 
from django.contrib.auth.decorators import login_required , user_passes_test
from register.models import Student
from instructor.models import *
from student.models import QuizResult , Comment
from django.core.files.storage import FileSystemStorage
from core.utils import *



@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def lesson_view(request, id):
    current_student = Student.objects.get(user=request.user)
    current_lesson = Lesson.objects.get(id=id)
    related_quiz = Quiz.objects.filter(lesson = current_lesson)
    passed_quiz_count = QuizResult.objects.filter(lesson = current_lesson, student = current_student, passed = "Passed").count()
    all_result = get_quiz_result(related_quiz, QuizResult, current_lesson, current_student)
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
    current_section = Section.objects.get(id=id)
    online = LiveMeeting.objects.filter(section=current_section).first()
    comments = Comment.objects.filter(section=current_section)
    return render(request, 'section_template.html', {'section': current_section, 'online': online, 'comments': comments})




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

