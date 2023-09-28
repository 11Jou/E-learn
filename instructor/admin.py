from django.contrib import admin
from .models import Course , Lesson , StudentCourseAccess, Question, Answer, Quiz, Choice, Section , CompleteCourse , LiveMeeting

admin.site.register(Course); admin.site.register(Lesson) ; admin.site.register(Section)
admin.site.register(StudentCourseAccess)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(Choice)
admin.site.register(CompleteCourse)
admin.site.register(LiveMeeting)

