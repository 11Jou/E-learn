# Generated by Django 4.2.4 on 2023-09-06 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_rename_superuser_instructor_staffuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='invited_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.instructor', to_field='staffuser'),
        ),
    ]
