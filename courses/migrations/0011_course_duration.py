# Generated by Django 2.2.1 on 2019-06-05 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_course_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
