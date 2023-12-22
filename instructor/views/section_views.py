from django.shortcuts import render , redirect
from register.models import Instructor , Student
from instructor.models import *
from student.models import Comment , Reply
from django.contrib.auth.models import User
from instructor.forms import CourseForm , LessonForm , SectionForm , OnlineSectionForm
from django.contrib.auth.decorators import login_required , user_passes_test
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator


# Upload Section by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def upload_section(request, id):
    form = SectionForm()
    form2 = OnlineSectionForm()
    current_lesson = Lesson.objects.get(id=id)
    sections = Section.objects.filter(lesson = current_lesson)
    if request.method == "POST":
        if "lesson-form" in request.POST:
            form = SectionForm(request.POST , request.FILES)
            if form.is_valid():
                section_name = form.cleaned_data['sectionName']
                section_content = form.cleaned_data['content']
                section_pdf = form.cleaned_data['pdf']
                section_video = form.cleaned_data['video']
                newSection = Section(lesson = current_lesson, sectionName = section_name, video=section_video, content=section_content, pdf=section_pdf)
                newSection.save()
            return redirect('upload_section', id=id)
        elif "lesson-form2" in request.POST:
            form2 = OnlineSectionForm(request.POST, request.FILES)
            if form2.is_valid():
                section_name2 = form2.cleaned_data['sectionName']
                section_content2 = form2.cleaned_data['content']
                section_pdf2 = form2.cleaned_data['pdf']
                start_time = form2.cleaned_data['start_time']
                url = form2.cleaned_data['url']
                newOnline = Section(lesson = current_lesson, sectionName = section_name2, video=None, 
                                    content=section_content2, pdf=section_pdf2)
                newOnline.save()
                newOnlineSection = LiveMeeting(section=newOnline, start_time=start_time, url=url) 
                newOnlineSection.save()
                return redirect('upload_section', id=id)

    return render(request, 'upload_section.html', {'form':form, 'form2':form2, 'sections':sections, 'lesson':current_lesson})

# Create quiz by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def create_quiz(request, id):
    lesson = Lesson.objects.get(id=id)
    if request.method == "POST":
        quiz_name = request.POST.get('quiz-name')
        questions = request.POST.getlist('questions[]')
        choices = []
        correct_answers = []
        for i in range(len(questions)):
            for j in range(3):
                choice_name = f'choices[{i}][{j}]'
                correct_answer = f'correct[{i}]'
                choice_text = request.POST.get(choice_name)
                answer = request.POST.get(correct_answer)
                if j == 0:
                    correct_answers.append(answer)
                choices.append(choice_text)
        newQuiz = Quiz(lesson=lesson, title=quiz_name)
        newQuiz.save()
        for i in range(len(questions)):
            correct_answer = correct_answers[i]
            question_text = questions[i]
            newQuestion = Question(quiz=newQuiz, content=question_text)
            newQuestion.save()
            for j in range(3):
                choice = choices[i * 3 + j]
                is_correct = j == int(correct_answer)
                newChoice = Choice(question=newQuestion, answer=choice, is_correct=is_correct)
                newChoice.save()
        student_access = StudentCourseAccess.objects.filter(lesson = lesson)
        completed_course = CompleteCourse.objects.filter(course = lesson.course.id)
        for i in completed_course:
                    i.delete()
        for studnet in student_access:
            studnet.is_complete = False
            studnet.save()
        return redirect('upload_section', id=id)
    return render(request, 'create_quiz.html', {'lesson': lesson})

# Delete section by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def delete_section(request, id):
    section = Section.objects.get(id=id)
    lessonId = section.lesson.id
    section.delete()
    return redirect('upload_section', id=lessonId)


@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def edit_section(request, id):
    section = Section.objects.get(id=id)
    lessonId = section.lesson.id
    if request.method == 'POST':
        section.sectionName = request.POST.get('section-name')
        section.content = request.POST.get('section-content')
        section.save()
        return redirect('upload_section', id=lessonId)
    return render(request, 'edit_section.html', {'section':section})


@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser and Instructor.objects.filter(staffuser=user).exists())
def instructor_section(request, id):
    current_section = Section.objects.get(id=id)
    online = LiveMeeting.objects.filter(section=current_section).first()
    comments = Comment.objects.filter(section=current_section)
    return render(request, 'instructor_section.html', {'section': current_section, 'comments':comments, 'online': online,})










