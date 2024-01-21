import random
import time
from datetime import datetime, timedelta

import django.contrib.auth
from django.db import models
from django.core import validators
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

import Accounts.models
Account = "Accounts.account"
import uuid


class EventsMembers(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    points = models.IntegerField(validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(100)
    ], null=True)
    is_active = models.BooleanField(default=False)


class ClassRoomsNumber(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return self.name


class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    methodists = models.ManyToManyField(Account, limit_choices_to={"role__label": "methodist"}, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Катигории"

    def __str__(self):
        return self.name


class Subjects(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class OrganizationScenario(models.Model):
    name = models.TextField(max_length=5550)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(default=False)

class Materials(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="materials/%Y/%m/%d/")
class Events(models.Model):
    CLASSROOM = [
        ("0", "Детский сад"),
        ("1", "1 класс"),
        ("2", "2 класс"),
        ("3", "3 класс"),
        ("4", "4 класс"),
        ("5", "5 класс"),
        ("6", "6 класс"),
        ("7", "7 класс"),
        ("8", "8 класс"),
        ("9", "9 класс"),
        ("10", "10 класс"),
        ("11", "11 класс")
    ]
    TYPES = [
        ("subject", "Предметное"),
        ("methodist", "Методическое")
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2550)

    start_date = models.DateTimeField(auto_now=False)
    end_date = models.DateTimeField(auto_now=False)

    classroom_number = models.CharField(max_length=255, choices=CLASSROOM, null=True)
    type = models.CharField(max_length=255, choices=TYPES, null=True, default="subject")

    archive = models.BooleanField(default=False)

    image = models.ImageField(upload_to="images", null=True)

    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, related_name="subject", blank=True)
    category = models.ForeignKey(EventCategory, related_name="category", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    organizer = models.ManyToManyField(Account, related_name="organizer")
    organizer_scenario = models.ManyToManyField(OrganizationScenario, related_name="organizer_scenario", blank=True)
    organizer_materials = models.ManyToManyField(Materials, related_name="organizer_materials", blank=True)


    building = models.ForeignKey("Accounts.building", on_delete=models.SET_NULL, related_name="building", null=True)

    volunteer = models.ManyToManyField(EventsMembers, related_name="volunteers", blank=True)

    def volunteer_count(self):
        return self.volunteer.count()

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.name} - {self.volunteer}"


def f(instance, filename):
    ext = filename.split('.')[-1]
    return '{}.{}'.format(f"photo_reports/{instance.event.pk}/{uuid.uuid4()}", ext)


class PhotoReport(models.Model):
    image = models.ImageField(upload_to=f)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)


@receiver(post_delete, sender=PhotoReport)
def delete_image_file(sender, instance, **kwargs):
    print("delete_image_file")
    instance.image.delete(False)


class ClassRoom(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="teacher", null=True)
    member = models.ManyToManyField(Account, related_name="students", blank=True)
    classroom = models.IntegerField()
    parallel = models.CharField(max_length=1)

    def invite_url(self):
        return f"https://mysite.com:8000/lk/classroom/invite/{self.uuid}/"

    def __str__(self):
        return f"{self.classroom}\"{self.parallel}\""

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"


class PsychologistSchedule(models.Model):
    psychologist = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="psychologist",
                                     limit_choices_to={"role": "psychologist"})
    child = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="child",
                              limit_choices_to=Q(peculiarity__in=["handicapped", "autism"]))
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    comment = models.TextField(max_length=2550, null=True, blank=True)

    def __str__(self):
        return f"{self.child} - {self.date}"

    def can_move(self):
        dt = datetime.now()
        if self.date <= dt.date():
            return False
        elif (self.date - dt.date()).days <= 2:
            print((self.date - dt.date()).days)
            return False
        else:
            return True


class TeacherInviteEvent(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="event_classroom")
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="event_teacher")

    class Meta:
        verbose_name = "Приглашение на мероприятие"
        verbose_name_plural = "Приглашения на мероприятия"


class FeedBackQuestions(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.TextField(max_length=2550)
    answer = models.TextField(max_length=2550, null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="user", null=True)
    answer_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="answer_by", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True)


    def __str__(self):
        return self.name

class ClassRoomTeacherAuthUser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="ct")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="clr")
    password = models.CharField(max_length=255)

class SystemReports(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    users_count = models.IntegerField()
    events_count = models.IntegerField()
    classrooms_count = models.IntegerField()
    teachers_count = models.IntegerField()
    staffs_count = models.IntegerField()
    students_count = models.IntegerField()
    students_in_events_count = models.IntegerField()
    accounts_have_admin_permissions = models.IntegerField()
    end_events_count = models.IntegerField()
    average_events_members_count = models.IntegerField()
    average_members_points = models.IntegerField()

    @staticmethod
    def create_report():
        users = Accounts.models.Account.objects.all()
        events = Events.objects.all()
        classrooms = ClassRoom.objects.all()
        students = users.filter(role="student").count()
        teachers = users.filter(role="teacher").count()
        staffs = users.filter(role="methodist").count()+users.filter(role="head_teacher").count()+users.filter(role="director").count()+users.filter(role="psychologist").count()+teachers
        classrooms_count = classrooms.count()
        events_count = events.count()
        end_events_count = events.filter(end_date__gt=timezone.now()).count()
        accounts_have_admin_permissions = users.filter(role="admin").count() + users.filter(role="director").count()
        students_in_events_count = [i.volunteer.count() for i in events]
        students_in_events_count = sum(students_in_events_count)
        average_events_members_count = students_in_events_count/students
        average_members_points = sum([i.points for i in users])/students
        SystemReports.objects.create(
            users_count = users.count(),
            events_count = events_count,
            classrooms_count = classrooms_count,
            teachers_count = teachers,
            staffs_count = staffs,
            students_count = students,
            students_in_events_count = students_in_events_count,
            accounts_have_admin_permissions = accounts_have_admin_permissions,
            end_events_count = end_events_count,
            average_events_members_count = average_events_members_count,
            average_members_points = average_members_points
        )

