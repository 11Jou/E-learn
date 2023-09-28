from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_course, name='student_course'),
    path('course-details/<int:id>', views.course_details, name='course_details'),
    path('lesson-view/<int:id>', views.lesson_view, name='lesson_view'),
    path('section-view/<int:id>', views.section_view, name='section_view'),
    path('add-comment/<int:id>', views.add_comment, name='add_comment'),
    path('add-reply/<int:id>', views.add_reply, name='add_replay'),
    path('view-reply/<int:id>', views.view_replies, name='view_reply'),
    path('pdf-view/<int:pdfId>', views.pdf_view, name='pdf_view'),

]