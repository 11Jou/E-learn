# Generated by Django 4.2.4 on 2023-09-15 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0004_remove_course_lesson_alter_course_coursename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        ),
    ]
