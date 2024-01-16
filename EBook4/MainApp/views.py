import string
from validate_email import validate_email
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EventAddForm
from .models import Events, FeedBackQuestions
from django.contrib.auth.decorators import login_required
from Accounts.models import Account
import requests
import os
spam_words = ["вебинар",]
def remove_punctuation(text):
    for i in string.punctuation:
        text = text.replace(i, ' ')
    return text
def check_email_exist(email):
    is_valid = validate_email(email, check_mx=True)
    return is_valid
def check_spam(text):
    text = remove_punctuation(text)
    text = text.lower()
    for i in spam_words:
        if i in text:
            return True
    return False

def index(request):
    if not requests.get(f"https://school1236.ru/school/{settings.TOKEN}").json().get("ok"): return HttpResponse(
        "Укажите токен школы!")
    return render(request, "main.html")

def feedback(request):
    if request.method == "POST":
        print(request.POST)
        user = None
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        if request.user.is_authenticated:
            user = request.user
        print(name, email, phone, message)
        if not check_spam(message) and check_email_exist(email):
            FeedBackQuestions.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
                user=user
            )

            text = f"Имя: {name}\nEmail: {email}\nТелефон: {phone}\nСообщение: {message}\n\nВопрос от {email}\n\n"
            r = requests.get(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/sendMessage?chat_id={settings.BOT_CHAT_ID}&text={text}")

        else:
            return HttpResponse("Спам")
        return redirect("/")


def token(request):
    return HttpResponse(settings.TOKEN)