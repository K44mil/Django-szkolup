# Generated by Django 2.2.1 on 2019-06-05 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='duration',
        ),
    ]