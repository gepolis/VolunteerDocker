from django.utils import timezone

from .models import SystemReports


def my_scheduled_job():
    SystemReports.create_report()
