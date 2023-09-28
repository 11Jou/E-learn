from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:id>', views.user_profile, name='user_profile'),
    path('student-quiz/<int:id>', views.answer_quiz, name='answer_quiz'),
    path('dashboard/<int:id>', views.student_performance, name='student_performance'),
    path('completed_courses/<int:id>', views.completed_courses, name='completed'),
    path('in_progress_courses/<int:id>', views.in_progress, name='in_progress'),
    path('student-answers/<int:id>/<int:studentId>', views.student_answers, name='student_answers')
]