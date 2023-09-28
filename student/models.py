from django.db import models
from instructor.models import Quiz , Lesson , Section
from django.contrib.auth.models import User
from register.models import Student

class QuizResult(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_mark = models.IntegerField()
    quiz_mark = models.IntegerField()
    passed = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{str(self.quiz)} - {str(self.student)}"
    
    class Meta:
        constraints  = [
            models.UniqueConstraint(fields=['quiz', 'student'], name='quiz and studnet')]
        

class Comment(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"{str(self.student)} - {str(self.section)}"
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"{str(self.person)} - {str(self.comment)}"