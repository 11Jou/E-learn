# Generated by Django 4.2.4 on 2023-09-28 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0007_alter_student_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 28, 16, 23, 52, 330872, tzinfo=datetime.timezone.utc)),
        ),
    ]
