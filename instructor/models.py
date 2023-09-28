from django.db import models
from django.contrib.auth.models import User
from register.models import Instructor, Student
from django.utils import timezone


class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    courseName = models.CharField(max_length=50)
    image = models.ImageField(upload_to='course_image/%Y/%m/%d/')
    description = models.TextField(max_length=500)
    Type = models.CharField(max_length=50)
    student_complete = models.ManyToManyField(Student, through="CompleteCourse")

    def __str__(self) -> str:
        return self.courseName

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    students = models.ManyToManyField(Student, through="StudentCourseAccess")

    def __str__(self) -> str:
        return f"{str(self.course)} - {self.name}"

    
class Section(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    sectionName = models.CharField(max_length=50)
    video = models.FileField(upload_to='videos/%Y/%m/%d/', null=True)
    content = models.TextField(max_length=1000)
    pdf = models.FileField(upload_to='pdfs/%Y/%m/%d/')


    def __str__(self) -> str:
        return f"{str(self.lesson)} - {self.sectionName}"
        
class LiveMeeting(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    url = models.URLField()

    def __str__(self) -> str:
        return f"{str(self.section)}"
    
class StudentCourseAccess(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    can_view_anytime = models.BooleanField(default=True)
    specific_time_start = models.DateTimeField(default=timezone.now)
    specific_time_end = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.student} - {self.lesson}"
    

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{str(self.lesson)} - {self.title}"
    

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{str(self.quiz)}"
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{str(self.question)} - {self.answer}"

    
class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='answer_to_question')
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{str(self.student)} - {str(self.question)}"
    
    class Meta:
        constraints  = [
            models.UniqueConstraint(fields=['student', 'question'], name='student and question')]
    

class CompleteCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    complete_time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{str(self.student)} - {str(self.course)}"

    class Meta:
        constraints  = [
            models.UniqueConstraint(fields=['student', 'course'], name='student and course')]
