# Generated by Django 4.2.4 on 2023-09-27 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0007_alter_student_photo'),
        ('instructor', '0018_alter_section_video'),
        ('student', '0003_quizresult_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.section')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.student')),
            ],
        ),
    ]
