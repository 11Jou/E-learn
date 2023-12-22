from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required , user_passes_test
from register.models import Student
from instructor.models import *
from student.models import QuizResult
from core.utils import *

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
        result = check_pass_quiz(correct_answers, questions)
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



