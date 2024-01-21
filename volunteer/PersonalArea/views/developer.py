import os

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from Accounts import decorators
from MainApp.models import FeedBackQuestions


@decorators.is_developer
def feedbacks(request):
    if request.method == "POST":
        selected = request.POST.get("selected")
        if selected is not None and selected.count(":") > 0:
            d = [int(i) for i in selected.split(":")]
            FeedBackQuestions.objects.filter(pk__in=d).delete()
            messages.success(request, "Вопросы удален")
    fbs = FeedBackQuestions.objects.all().filter(answer__isnull=True)
    return render(request, "developer/feedbacks.html", {"fbs": fbs, "archive": False, "section": "feedbacks"})


@decorators.is_developer
def feedbacks_archive(request):
    fbs = FeedBackQuestions.objects.all().filter(answer__isnull=False).order_by("-answered_at")
    return render(request, "developer/feedbacks.html", {"archive": True, "fbs": fbs, "section": "archive"})


@decorators.is_developer
def view_feedback(request, fb_id):
    fb = FeedBackQuestions.objects.get(pk=fb_id)
    return render(request, "developer/view_feedback.html", {"fb": fb, "section": "feedbacks"})


@decorators.is_developer
def send_feedback_answer(request, fb_id):
    if request.method == "POST":
        fb = FeedBackQuestions.objects.get(pk=fb_id)
        answer = request.POST.get("answer")
        if send_mail("Ответ на Ваш вопрос", answer, settings.EMAIL_HOST_USER, [fb.email]):
            messages.success(request, "Ответ отправлен")
            fb.answer = answer
            fb.answered_at = timezone.now()
            fb.answer_by = request.user
            fb.save()
        else:
            messages.error(request, "Ошибка отправки")
        return redirect("/lk/feedbacks/")


@decorators.is_developer
def get_logs(request):
    el_col = {
        "GET": "green",
        "POST": "skyblue",
        "200": "green",
        "301": "red",
        "302": "red",
        "403": "red",
        "404": "red",
        "500": "darkred",
        'HTTP': "#CEACE6",
        '304': "red",  # 304 - Not Modified

    }
    lines = []
    logs = ""
    with open("/root/Ebook1/nohup.out", "r") as f:
        lines = f.readlines()[-100:] # last 100 lines
    logs = "<br>".join(lines)

    for i in el_col:
        logs = logs.replace(i, f"<span style='color: {el_col[i]}'>{i}</span>")
    return render(request, "developer/logs.html", {"section": "logs", "logs": logs})


def drag(request):
    return render(request, "developer/drag.html")


def developer(request):
    return render(request, "developer/index.html")


def drop(request, setting, value):
    if request.method == "POST":
        pass
    else:
        return redirect("/lk/")