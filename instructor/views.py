from django.shortcuts import render , redirect
from register.models import Instructor , Student
from .models import Course , Lesson , StudentCourseAccess , Section , Quiz , Question , Choice , CompleteCourse , LiveMeeting
from student.models import Comment , Reply
from django.contrib.auth.models import User
from .forms import CourseForm , LessonForm , SectionForm , OnlineSectionForm
from django.contrib.auth.decorators import login_required , user_passes_test
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator

# View Course of logged in instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def course_view(request):
    current_instructor = Instructor.objects.get(staffuser = request.user)
    courses = Course.objects.filter(instructor = current_instructor)
    return render(request , 'instructor_course.html', {'courses':courses})

# Delete Course from instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('instructor_courses')


# View instructor's students
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def student_view(request):
    current_instructor = Instructor.objects.get(staffuser = request.user)
    students = Student.objects.filter(invited_by = current_instructor).order_by('name')
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request , 'all_student.html', {'students':students})

# Upload course by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
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


# Upload lesson by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
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
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def delete_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    courseId = lesson.course.id
    lesson.delete()
    return redirect('upload_lesson' ,id=courseId)


# Edit lesson by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def edit_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    courseId = lesson.course.id
    if request.method == "POST":
        lesson.name = request.POST.get('lesson_name')
        lesson.content = request.POST.get('lesson_content')
        lesson.save()
        return redirect('upload_lesson' ,id=courseId)
    return render(request, 'edit_lesson.html', {'lesson':lesson})


# Upload Section by instructor
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
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
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
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
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def delete_section(request, id):
    section = Section.objects.get(id=id)
    lessonId = section.lesson.id
    section.delete()
    return redirect('upload_section', id=lessonId)


@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
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
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def instructor_section(request, id):
    current_section = Section.objects.get(id=id)
    online = LiveMeeting.objects.filter(section=current_section).first()
    comments = Comment.objects.filter(section=current_section)
    return render(request, 'instructor_section.html', {'section': current_section, 'comments':comments, 'online': online,})



@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def delete_student(request, id):
    deleted_student = User.objects.get(id=id)
    deleted_student.delete()
    return redirect('instructor_student')






