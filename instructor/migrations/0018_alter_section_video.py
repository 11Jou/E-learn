# Generated by Django 4.2.4 on 2023-09-26 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0017_livemeeting_start_time_alter_livemeeting_roomid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='video',
            field=models.FileField(null=True, upload_to='videos/%Y/%m/%d/'),
        ),
    ]
