# Generated by Django 4.2.7 on 2023-11-13 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainApp', '0010_psychologistschedule_feedbackquestions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='materials/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationScenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=5550)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='events',
            name='organizer',
        ),
        migrations.AddField(
            model_name='events',
            name='organizer_materials',
            field=models.ManyToManyField(blank=True, related_name='organizer_materials', to='MainApp.materials'),
        ),
        migrations.AddField(
            model_name='events',
            name='organizer_scenario',
            field=models.ManyToManyField(blank=True, related_name='organizer_scenario', to='MainApp.organizationscenario'),
        ),
        migrations.AddField(
            model_name='events',
            name='organizer',
            field=models.ManyToManyField(related_name='organizer', to=settings.AUTH_USER_MODEL),
        ),
    ]