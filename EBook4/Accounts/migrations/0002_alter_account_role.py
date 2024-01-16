# Generated by Django 4.2 on 2023-07-05 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.TextField(choices=[('admin', 'Администратор'), ('teacher', 'Учитель'), ('parent', 'Родитель'), ('student', 'Ученик'), ('methodist', 'Методист'), ('director', 'Директор'), ('head_teacher', 'Завуч')], max_length=20, null=True),
        ),
    ]
