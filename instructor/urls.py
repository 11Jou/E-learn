from django.urls import path
from .views import *

urlpatterns = [
    path('courses', course_view, name='instructor_courses'),
    path('delete-course/<int:id>', delete_course, name='delete_course'),
    path('students', student_view, name='instructor_student'),
    path('delete-student/<int:id>', delete_student, name='delete_student'),
    path('new-course', upload_course, name='upload_course'),
    path('new-lesson/<int:id>', upload_lesson, name='upload_lesson'),
    path('new-section/<int:id>', upload_section, name='upload_section'),
    path('delete-lesson/<int:id>', delete_lesson, name='delete'),
    path('edit-lesson/<int:id>', edit_lesson, name='edit'),
    path('delete-section/<int:id>', delete_section, name='delete_section'),
    path('edit-section/<int:id>', edit_section, name='edit_section'),
    path('instructor-section/<int:id>', instructor_section, name='instructor_section'),
    path('create-quiz/<int:id>', create_quiz, name='create_quiz'),
]