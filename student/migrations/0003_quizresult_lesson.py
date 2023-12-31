# Generated by Django 4.2.4 on 2023-09-24 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0013_alter_answer_question_alter_answer_student_answer'),
        ('student', '0002_alter_quizresult_student_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='lesson',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='instructor.lesson'),
            preserve_default=False,
        ),
    ]
