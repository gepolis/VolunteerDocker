# Generated by Django 5.0.1 on 2024-01-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('short_name', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('mos_ru_auth', models.BooleanField(default=True)),
                ('token', models.CharField(max_length=1000)),
            ],
        ),
    ]
