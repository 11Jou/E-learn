from django.shortcuts import render ,redirect
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required , user_passes_test
from register.models import Student , Instructor
from instructor.models import Quiz, Question, Choice, Answer , CompleteCourse , Course , Lesson
from .models import QuizResult

# Create your views here.
@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def user_profile(request, id):
    current_user = User.objects.get(id=id)
    current_student = Student.objects.get(user = current_user)
    related_instructor = Instructor.objects.get(id=current_student.invited_by.id)
    previous_username = current_user.username ; previous_mail = current_user.email
    if request.method == "POST":
        current_student.name = request.POST.get('name')
        current_user.username = request.POST.get('username')
        current_user.email = request.POST.get('email')
        photo = request.FILES.get('photo')
        if photo:
            current_student.photo = photo
        if User.objects.filter(username = current_user.username).exists() and current_user.username != previous_username or User.objects.filter(email = current_user.email).exists() and current_user.email != previous_mail :
                return render(request, 'user_profile.html', {'student':current_student, 'instructor':related_instructor,
                                                            'message':'Username or Email is already exist'})
        current_student.save()
        current_user.save()
        return redirect('user_profile', id=current_user.id)
    return render(request, 'user_profile.html', {'student':current_student, 'instructor':related_instructor})

@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def answer_quiz(request,id):
    current_quiz = Quiz.objects.get(id=id)
    related_lesson = Lesson.objects.get(id = current_quiz.lesson.id)
    questions = Question.objects.filter(quiz=current_quiz)
    correct_answers = 0
    if request.method == "POST":
        current_student = Student.objects.get(user = request.user)
        for question in questions:
            choice_id = request.POST.get(f'{question.id}', None)
            if choice_id:
                studnet_choice = Choice.objects.get(id=choice_id)
                previous_answer = Answer.objects.filter(student = current_student, question=question).exists()
                if previous_answer:
                    previous_answer = Answer.objects.get(student = current_student, question=question)
                    previous_answer.student_answer = studnet_choice
                    previous_answer.is_correct =  studnet_choice.is_correct
                    previous_answer.save()
                else:
                    newAnswer = Answer(student=current_student, question=question, student_answer = studnet_choice, is_correct = studnet_choice.is_correct)
                    newAnswer.save()
                if studnet_choice.is_correct:
                    correct_answers += 1
                
        if correct_answers >= 0.5 * questions.count():
            result = "Passed"
        else:
            result = "Not Passed"
        check_exist = QuizResult.objects.filter(lesson = related_lesson, quiz = current_quiz , student = current_student)
        if check_exist:
            check_exist = QuizResult.objects.get(lesson = related_lesson, quiz = current_quiz , student = current_student)
            check_exist.student_mark = correct_answers
            check_exist.passed = result
            check_exist.save()
        else:
            newResult = QuizResult(lesson = related_lesson, quiz = current_quiz, student = current_student, 
                                student_mark = correct_answers, quiz_mark = questions.count(), passed = result)
            newResult.save()
        return redirect('lesson_view', id= current_quiz.lesson.id)
    quiz_to_answer = {}
    for q in questions:
        quiz_to_answer[q] = []
        choices = Choice.objects.filter(question=q)
        for choice in choices:
            quiz_to_answer[q].append(choice)        
    return render(request, 'answer_quiz.html' ,{'quiz_name':current_quiz.title, 'quiz':quiz_to_answer})

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
