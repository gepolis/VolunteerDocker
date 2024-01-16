from MainApp.models import FeedBackQuestions
from django import template

register = template.Library()


@register.simple_tag
def questions_count():
    c = FeedBackQuestions.objects.all().filter(answer__isnull=True).count()
    if c == 0:
        return '0'
    if c >= 100:
        return "99+"
    if c >= 10:
        return "9+"
    return f"{c}"

@register.simple_tag
def qc():
    c = FeedBackQuestions.objects.all().filter(answer__isnull=True).count()
    return int(c)


