from django.urls import path
from . import views

urlpatterns = [
    path('courses', views.course_view, name='instructor_courses'),
    path('delete-course/<int:id>', views.delete_course, name='delete_course'),
    path('students', views.student_view, name='instructor_student'),
    path('delete-student/<int:id>', views.delete_student, name='delete_student'),
    path('new-course', views.upload_course, name='upload_course'),
    path('new-lesson/<int:id>', views.upload_lesson, name='upload_lesson'),
    path('new-section/<int:id>', views.upload_section, name='upload_section'),
    path('delete-lesson/<int:id>', views.delete_lesson, name='delete'),
    path('edit-lesson/<int:id>', views.edit_lesson, name='edit'),
    path('delete-section/<int:id>', views.delete_section, name='delete_section'),
    path('edit-section/<int:id>', views.edit_section, name='edit_section'),
    path('instructor-section/<int:id>', views.instructor_section, name='instructor_section'),
    path('create-quiz/<int:id>', views.create_quiz, name='create_quiz'),

]