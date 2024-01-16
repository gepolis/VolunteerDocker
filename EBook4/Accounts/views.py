from datetime import datetime
from threading import Thread

import django_user_agents.utils
import requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import *
from .models import *
from .utils import get_profile_data
from MainApp.models import ClassRoom
from rest_framework.authtoken.models import Token


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


def register_request(request):
    if request.user.is_authenticated:
        return redirect("/lk/choice/")

    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            if settings.ROLES_PASSWORDS.get(request.POST.get("role")) != request.POST.get("code"):
                messages.error(request, "Неверный код подтверждения!")

                return redirect("/auth/?m=reg")
            user = form.save()
            user.role = request.POST.get("role")
            user.save()
            login(request, user)
            add_connection(request)
            messages.success(request, 'Вы успешно зарегистрировались!')
            r = redirect("/lk/choice/")
            r.set_cookie("token", get_or_generate_token(request), max_age=60 * 60 * 24 * 7 * 30)
            return r
        else:
            messages.success(request, f'Ошибка({form.errors})!')

            return redirect("/auth/?m=reg")
    else:
        return HttpResponse("m")


def auth(request):
    if request.user.is_authenticated:
        return redirect("/lk/choice/")
    context = {
        "register_form": NewUserForm(),
        "login_form": AccountSignInForm()
    }
    return render(request, "auth.html", context=context)


def auth_mos_ru(request):
    # messages.error(request, "Авторизация через mos.ru временно не работает, пожалуйста, используйте другой способ авторизации или попробуйте позже.")
    # return redirect("/auth/")
    if request.user.is_authenticated:
        return redirect("/lk/choice/")

    if request.method == "GET":
        context = {
            "login_form": AccountMosRuForm()
        }
        return render(request, "mos_ru_auth.html", context=context)
    else:
        login, passowrd = request.POST.get("login"), request.POST.get("password")
        mraa = MosRuAuthAPI(login, passowrd)
        u = mraa.create()
        mraa.start()

        context = {
            "uuid": u
        }
        return render(request, "mos_ru_auth_wait.html", context=context)


def mos_ru_status(request, uuid):
    m = MosRuAuthAPI.get(uuid)
    return JsonResponse(m)


class MosRuAuthAPI:
    def __init__(self, login, password):
        self.login = login
        self.uuid = None
        self.password = password

    def create(self):
        m = MosRuAuth.objects.create()
        self.uuid = str(m.uuid)
        return m.uuid

    def start(self):
        t = Thread(target=get_profile_data, args=(self.login, self.password, self.uuid))
        t.start()

    @staticmethod
    def get(uuid):
        m = MosRuAuth.objects.get(uuid=uuid)
        d = {
            "uuid": m.uuid,
            "status": m.status,
            "captcha": False,
        }
        if m.captcha:
            d["captcha"] = True
            d["captcha_url"] = m.captcha_url
        return d


def mos_ru_login(request, uuid):
    m = MosRuAuth.objects.get(uuid=uuid)
    data = m.data
    fn = data.get("profile").get("first_name")
    ln = data.get("profile").get("last_name")
    mn = data.get("profile").get("middle_name")
    email = data.get("profile").get("email")
    classroom_number, classroom_paralell = data.get("children")[0].get('class_name').split("-")
    role = data.get("profile").get("type")
    school = data.get("children")[0].get("school").get("short_name")
    token = data.get("token")
    if school == "ГБОУ Школа № 1236":
        if not Account.objects.all().filter(email=email).exists():

            username = f"user_{Account.objects.all().count()}"
            auth_user = Account(email=email, username=username, first_name=fn,
                                second_name=ln, middle_name=mn,
                                role=role, password="mos.ru", token=data.get("token"))
            auth_user.save()
            login(request, auth_user)

            if role == "student":
                building = None
                for key, value in settings.BUILDINGS_PARALELS.items():
                    if classroom_paralell in value:
                        auth_user.building = Building.objects.get(pk=key)
                        auth_user.save()
                        break

                classroom_number = int(classroom_number)

                classroom = ClassRoom.objects.all().filter(parallel=classroom_paralell,
                                                           classroom=classroom_number)

                if classroom.exists():
                    classroom = classroom.first()
                    classroom.member.add(auth_user)
                else:
                    classroom = ClassRoom(parallel=classroom_paralell, classroom=classroom_number)
                    classroom.save()
                    classroom.member.add(auth_user)
                    classroom.save()
                c = redirect("/lk/choice/")
                c.set_cookie("token", get_or_generate_token(request), max_age=60 * 60 * 24 * 7 * 30)
                return c

        else:
            auth_user = Account.objects.get(email=email)
            login(request, auth_user)

        c = redirect("/lk/choice/")
        c.set_cookie("token", get_or_generate_token(request), max_age=60 * 60 * 24 * 7 * 30)
        return c
    return HttpResponse(data)


def login_request(request):
    if request.user.is_authenticated:
        return redirect("/lk/choice/")

    if request.method == "POST":
        form = AccountSignInForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                ip = get_client_ip(request)
                if not Connections.objects.all().filter(ip=get_client_ip(request), user=user).exists():
                    add_connection(request)
                else:
                    add_connection(request)
                messages.success(request, 'Вы успешно вошли!')
                r = redirect("/lk/choice/")
                r.set_cookie("token", get_or_generate_token(request), max_age=60 * 60 * 24 * 7 * 30)
                return r
            else:
                messages.warning(request, "Пользователь не найден.")
        else:
            messages.warning(request, "Пользователь не найден.")
    form = AuthenticationForm()
    return redirect("/auth/?m=reg")


@login_required
def logout_request(request):
    Connections.objects.all().filter(user=request.user, session_key=request.session.session_key).delete()
    logout(request)
    messages.success(request, "Вы успешно вышли!")
    c = redirect("/")
    c.set_cookie("token", "", max_age=0)
    return c


@login_required
def setup(request):
    if request.method == "GET":
        if request.user.email is None or request.user.email == "":
            return render(request, "setup/email.html")
        elif request.user.second_name is None or request.user.second_name == "":
            return render(request, "setup/second_name.html")
        elif request.user.first_name is None or request.user.first_name == "":
            return render(request, "setup/first_name.html")
        elif request.user.middle_name is None or request.user.middle_name == "":
            return render(request, "setup/middle_name.html")
        else:
            return redirect("/")
    else:
        t = request.POST['type']
        if t == "email":
            if not Account.objects.all().filter(email=request.POST['email']).exists():
                user = request.user
                user.email = request.POST['email']
                user.save()
                return redirect("setup")
            else:
                return HttpResponse(request.POST['email'])
        elif t == "fn":
            user = request.user
            user.first_name = request.POST['fn']
            user.save()
            return redirect("setup")
        elif t == "sn":
            user = request.user
            user.second_name = request.POST['sn']
            user.save()
            return redirect("setup")
        elif t == "mn":
            user = request.user
            user.middle_name = request.POST['mn']
            user.save()
            return redirect("setup")
        else:
            return redirect("/")


@login_required
def user_activity(request):
    if Connections.objects.all().filter(user=request.user, session_key=request.session.session_key).exists():
        con = Connections.objects.get(user=request.user, session_key=request.session.session_key)
        if request.COOKIES.get("activity") is None:
            con.last_activity = datetime.now()
            con.save()
            j = JsonResponse({"status": "ok", "code": 1}, status=200, safe=False)
            j.set_cookie("activity", "ok", max_age=60)
        else:
            j = JsonResponse({"status": "cancel", "code": 2}, status=200, safe=False)
        j.set_cookie("welcome_screen", "", max_age=60 * 30)  # 30 min - 60*30
        return j
    else:
        return JsonResponse({"status": "error"}, status=400, safe=False)


def mos_ru_info(request):
    return render(request, "mos_ru_auth_info.html")

