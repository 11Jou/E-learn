# Generated by Django 4.2.4 on 2023-09-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0010_remove_answer_answer_answer_student_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourseaccess',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
