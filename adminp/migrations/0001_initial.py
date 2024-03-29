# Generated by Django 2.2.1 on 2019-06-04 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('time', models.DateTimeField()),
                ('read', models.BooleanField(default=False)),
            ],
        ),
    ]
