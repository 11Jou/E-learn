# Generated by Django 4.2.4 on 2023-09-28 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0009_alter_invitation_expiration_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expiration_datetime',
            field=models.DateTimeField(blank=True),
        ),
    ]
