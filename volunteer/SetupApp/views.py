import requests
from django.shortcuts import render, redirect, HttpResponse
from Accounts.models import Role, Connections
from .forms import NewSetupUser, SchoolInfoForm
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
import django_user_agents.utils
from django.conf import settings as dsettings
def setup_roles_view(request):
    if Role.objects.all().count() != 7:
        Role(name='Учитель', label="teacher").save()
        Role(name="Психолог", label="psychologist").save()
        Role(name="Директор", label="director").save()
        Role(name="Администратор",label="admin").save()
        Role(name="Завуч", label="head_teacher").save()
        Role(name="Методист", label="methodist").save()
        Role(name="Ученик", label="student").save()
    return redirect("/setup/account/create/")
# Create your views here.
def index(request):
    if not requests.get(f"https://school1236.ru/school/{dsettings.TOKEN}").json().get("ok"): return HttpResponse("Укажите токен школы!")
    return render(request, 'setup/index.html')

def get_or_generate_token(request):
    token, created = Token.objects.get_or_create(user=request.user)

    return token.key
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_connection(request):
    ip = get_client_ip(request)
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    ua = django_user_agents.utils.parse(ua_string)

    Connections.objects.create(ip=ip, user=request.user, session_key=request.session.session_key,
                               device_system=request.user_agent.os.family,
                               device_browser=request.user_agent.browser.family).save()



def account(request):
    if request.user.is_authenticated:
        if not requests.get(f"https://school1236.ru/school/{dsettings.TOKEN}").json().get("ok"): return HttpResponse(
            "Укажите токен школы!")
        return redirect("/lk/choice/")
    elif request.method == "POST":
        form = NewSetupUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            add_connection(request)
            r = redirect("/setup/school/settings")
            r.set_cookie("token", get_or_generate_token(request), max_age=60 * 60 * 24 * 7*30)
            return r
        else:
            return redirect("setup/account/create/")
    else:
        form = NewSetupUser()
        return render(request,"setup/create_account.html",{"form": form})


def settings(request):
    if request.method == "POST":
        form = SchoolInfoForm(request.POST)
        if form.is_valid():
            if not requests.get(f"https://school1236.ru/school/{dsettings.TOKEN}").json().get(
                "ok"): return HttpResponse("Укажите токен школы!")
            user = form.save()
            return redirect("/")
        else:
            return redirect("/setup/school/settings")
    else:
        form = SchoolInfoForm()
        return render(request,"setup/settings.html",{"form": form})
