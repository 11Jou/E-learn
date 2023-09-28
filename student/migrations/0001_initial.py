# Generated by Django 4.2.4 on 2023-09-24 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0007_alter_student_photo'),
        ('instructor', '0013_alter_answer_question_alter_answer_student_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_mark', models.IntegerField(default=0)),
                ('quiz_mark', models.IntegerField()),
                ('passed', models.CharField(max_length=20)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='quizresult',
            constraint=models.UniqueConstraint(fields=('quiz', 'student'), name='quiz and studnet'),
        ),
    ]
