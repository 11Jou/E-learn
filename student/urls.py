from django.urls import path
from .views import *


urlpatterns = [
    path('profile/<int:id>', user_profile, name='user_profile'),
    path('student-quiz/<int:id>', answer_quiz, name='answer_quiz'),
    path('dashboard/<int:id>', student_performance, name='student_performance'),
    path('completed_courses/<int:id>', completed_courses, name='completed'),
    path('in_progress_courses/<int:id>', in_progress, name='in_progress'),
    path('student-answers/<int:id>/<int:studentId>', student_answers, name='student_answers')
]