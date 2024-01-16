from SetupApp.models import SchoolInfo
from django import template

register = template.Library()


@register.simple_tag
def school_number():
    return f"{SchoolInfo.objects.all().first().number}"

