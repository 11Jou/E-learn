from django.shortcuts import render
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required 
from register.models import *
from instructor.models import *
from student.models import QuizResult


@login_required
def student_performance(request, id):
    current_student = Student.objects.get(user = id)
    completed_course = CompleteCourse.objects.filter(student = current_student)
    in_progress = Course.objects.filter(instructor=current_student.invited_by).exclude(id__in=completed_course.values_list('course_id',flat=True))
    quiz_grades = QuizResult.objects.filter(student = current_student)
    return render(request, 'dashboard.html', {'completed':completed_course, 'in_progress':in_progress, 
                                            'student':current_student, 'quizs':quiz_grades})

@login_required
def completed_courses(request, id):
    current_student = Student.objects.get(id = id)
    completed_course = CompleteCourse.objects.filter(student = current_student)
    completed_course_data = [
        {
            'id':course.id,
            'course' : course.course.courseName,
        }
        for course in completed_course
    ]
    return JsonResponse(completed_course_data, safe=False)

@login_required
def in_progress(request, id):
    current_student = Student.objects.get(id = id)
    completed_course_ids = CompleteCourse.objects.filter(student=current_student).values_list('course_id', flat=True)
    in_progress = Course.objects.filter(instructor=current_student.invited_by).exclude(id__in=completed_course_ids)
    in_progress_data = [{
        'id':course.id,
        'course' : course.courseName,
    }
    for course in in_progress
    ]
    return JsonResponse(in_progress_data, safe=False)


@login_required
def student_answers(request, id , studentId):
    current_student = Student.objects.get(id = studentId)
    related_quiz = Quiz.objects.get(id=id)
    questions = Question.objects.filter(quiz = related_quiz)
    question_choice = {}
    for question in questions:
        answer = Answer.objects.get(student = current_student, question=question)
        question_choice[question] = [answer.student_answer.answer, answer.is_correct]
    return render(request, 'student_answers.html',{'quiz_answer':question_choice})
