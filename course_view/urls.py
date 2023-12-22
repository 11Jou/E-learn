from django.urls import path
from .views import *

urlpatterns = [
    path('', student_course, name='student_course'),
    path('course-details/<int:id>', course_details, name='course_details'),
    path('lesson-view/<int:id>', lesson_view, name='lesson_view'),
    path('section-view/<int:id>', section_view, name='section_view'),
    path('add-comment/<int:id>', add_comment, name='add_comment'),
    path('add-reply/<int:id>', add_reply, name='add_replay'),
    path('view-reply/<int:id>', view_replies, name='view_reply'),
    path('pdf-view/<int:pdfId>', pdf_view, name='pdf_view'),

]