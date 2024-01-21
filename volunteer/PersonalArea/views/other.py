import json
import math
from datetime import datetime
import io
from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.core.paginator import Paginator

from SetupApp.models import SchoolInfo
from . import aam
import xlsxwriter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.utils.formats import localize

from Accounts import decorators
from Accounts.models import Building, Connections
from MainApp.models import *
from PersonalArea.forms import *
from PersonalArea.models import Message
from Accounts import utils
from django.conf import settings


@login_required
@decorators.has_role
def index(request):
    if not requests.get(f"https://school1236.ru/school/{settings.TOKEN}").json().get("ok"): return HttpResponse(
        "Укажите токен школы!")
    if request.user.role == "admin" or request.user.role == "director":
        item = Account.objects.all().filter(points__gt=0).order_by("-points")[:10]
        context = {
            "users": Account.objects.all().filter(is_superuser=False).count(),
            "events": Events.objects.all().count(),
            "reqs": EventsMembers.objects.all().filter(is_active=False).count(),
            "builds": Building.objects.all().count(),
            "students": item,
            "section": "index"
        }
        return render(request, "adminpanel/index.html", context)
    elif request.user.role == "teacher":

        context = {
            "section": "index"
        }
        if request.user.has_classroom():
            classroom = ClassRoom.objects.get(teacher=request.user)
            item = classroom.member.all()
            context['students'] = item
        return render(request, "teacher/index.html", context=context)
    elif request.user.role == "student":
        context = {
            "section": "index"
        }
        # return render(request, "chat.html")
        return render(request, "student/index.html", context=context)
    elif request.user.role == "methodist":
        context = {
            "section": "index"
        }
        return render(request, "methodist/index.html", context)
    elif request.user.role == "psychologist":
        context = {
            "section": "index"
        }
        return render(request, "psychologist/index.html", context)
    elif request.user.role == "head_teacher":
        item = Account.objects.all().filter(points__gt=0).order_by("-points")[:10]
        context = {
            "section": "index",
            "events": Events.objects.all().filter(building=request.user.building).count(),
            "students": Account.objects.all().filter(building=request.user.building, role="student").count(),
            "teachers": Account.objects.all().filter(building=request.user.building, role="teacher").count(),
            "psychologists": Account.objects.all().filter(building=request.user.building, role="psychologist").count(),
            "students_data": item

        }
        return render(request, "head_teacher/index.html", context)


def chat(request):
    if request.user.role in ["teacher", "student"]:
        room = request.user.get_classroom().id
    else:
        room = "staff"
    msgs = Message.objects.all().filter(room=room).order_by("date_added")
    return render(request, "chat.html", context={"msgs": msgs, "section": "chat", "room": room})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
def edit_profile(request):
    if request.method == "GET":
        form = EditProfileForm(instance=request.user)

    else:
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            return render(request, "settings.html", {"form": form})
        return redirect("/lk/settings/")
    return render(request, "settings.html", {"form": form})


@login_required
def events(request):
    e = Events.objects.all().filter(end_date__gt=timezone.now(), start_date__gt=timezone.now())

    if request.user.role == "teacher":
        if request.user.has_classroom():
            classroom = ClassRoom.objects.get(teacher=request.user)
            buildings = Building.objects.all()

            if request.GET.get("building"):
                if request.GET.get("building") != "all":
                    classroom = ClassRoom.objects.get(teacher=request.user)
                    building = request.GET.get("building")
                    e = e.filter(classroom_number=classroom.classroom, building=Building.objects.get(pk=building))
                else:
                    building = "all"

                paginator = Paginator(e, settings.ITEMS_FOR_PAGE)  # Show 25 contacts per page.
                page_number = request.GET.get("page")
                if page_number is None:
                    page_number = 1
                page_obj = paginator.get_page(page_number)
                return render(request, "teacher/events.html",
                              {"events": page_obj, "section": "events", "buildings": buildings, "building": building})
            else:
                e = e.filter(classroom_number=classroom.classroom, start_date__gt=datetime.now(),
                             end_date__gt=timezone.now())
                return render(request, "teacher/events.html",
                              {"events": e, "section": "events", "buildings": buildings})
        else:
            return redirect("/lk/classroom/create/")
    elif request.user.role == "student":
        if request.user.has_classroom():
            classroom = ClassRoom.objects.get(member=request.user)
            e = e.filter(classroom_number=classroom.classroom)
            return render(request, "student/events.html", {"events": e, 'section': 'events'})
        else:
            messages.warning(request, "Сначала вступите в класс, по приглашению от классного руководителя.")
            return redirect("/lk/")
    else:
        return aam.events_list(request)


@login_required
def all_events(request):
    e = Events.objects.all()
    mode = request.GET.get("mode")
    if mode == "my":
        em = EventsMembers.objects.all().filter(user=request.user)
        e = e.filter(volunteer__in=em)
    elif mode == "student":
        student = request.GET.get("student")
        if student is not None:
            student = Account.objects.get(pk=student)
            em = EventsMembers.objects.all().filter(user=student)
            e = e.filter(volunteer__in=em)
        else:
            return JsonResponse({}, safe=False)

    elif mode == "org":
        e = Events.objects.all().filter(organizer=request.user)
        print(len(e))
    out = []
    for event in e:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end_date.strftime("%m/%d/%Y, %H:%M:%S"),
        })
    if request.user.peculiarity is not None:
        for p in PsychologistSchedule.objects.all().filter(child=request.user):
            start_time = datetime.combine(p.date, p.start_time)
            end_time = datetime.combine(p.date, p.end_time)
            out.append({
                'title': "Психолог",
                'id': p.pk,
                'start': start_time,
                'end': end_time,
            })

    return JsonResponse(out, safe=False)


@login_required
def classroom_view_export(request, user):
    user = Account.objects.get(pk=user)
    events = Events.objects.all().filter(volunteer__in=EventsMembers.objects.all().filter(user=user, is_active=True))
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Название')
    worksheet.write('B1', 'Начало')
    worksheet.write('C1', 'Конец')
    worksheet.write('D1', 'Статус')
    worksheet.write('E1', 'Баллов')
    m = 1
    points = 0
    for i in events:
        m += 1
        wait = events.filter(pk=i.pk, start_date__gt=datetime.now()).exists()
        ended = events.filter(pk=i.pk, end_date__lt=datetime.now()).exists()
        # started = events.filter(pk=i.pk,end_date__gt=datetime.now(), start_date__lte=datetime.now()).exists()
        if wait:  # wait
            worksheet.write(f'D{m}', "Ожидание начала")
        elif ended:  # end
            worksheet.write(f'D{m}', "Завершено")
        else:  # start
            worksheet.write(f'D{m}', "Началось")

        if i.volunteer.get(user=user).points is not None:
            points += i.volunteer.get(user=user).points
            worksheet.write(f'E{m}', i.volunteer.get(user=user).points)
        else:
            worksheet.write(f"E{m}", "-")
        worksheet.write(f"B{m}", localize(i.start_date))
        worksheet.write(f"C{m}", localize(i.end_date))
        worksheet.write(f'A{m}', i.name)
    worksheet.autofit()
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'{user.full_name()}.xlsx')


@login_required
def event_detail(request, id):
    event = get_object_or_404(Events, pk=id)
    context = {
        "section": "events",
        "event": event,
        "report": PhotoReport.objects.all().filter(event=event, deleted=False),
        "end": Events.objects.all().filter(pk=event.pk, end_date__lt=datetime.now()).exists()
    }
    return render(request, "event_detail.html", context=context)


@login_required
def avatar_remove(request):
    user = request.user
    user.avatar = None
    user.save()
    return redirect("/lk/settings/")


@login_required
def devices(request):
    devices = Connections.objects.all().filter(user=request.user).order_by("-last_activity")
    return render(request, "devices.html", {"devices": devices})


def delete_device(request, device):
    connection = get_object_or_404(Connections, session_key=device)
    connection.delete()
    Session.objects.all().filter(session_key=device).delete()
    messages.success(request, "Устройство удалено.")
    return redirect("/lk/settings/security/devices")


@login_required
def settings_linking_mosru(request):
    if request.method == "POST":
        form = LinkingMosruForm(request.POST)
        login, password = request.POST["login"], request.POST["password"]
        data = utils.get_profile_data(login, password)

        if data:
            if Account.objects.filter(token=data.get("authentication_token")).exists():
                messages.error(request, "Данный аккаунт МЭШ уже привязан!")
            else:
                headers = {
                    # "Authorization": "MTA2Njg0NDI5OTUxMTIyMjI5NA.G8T_2D.HCBJ-AP1RhRXABiJhWfTS80SD1kJ8Gk4QHA6eo",
                    "Authorization": "Bot MTE0NTQ3MTMwMDcwMjMyNjkzNw.GQSnnl.SJt9a0Ul8kxCZVvnBgnXcdV3EcsS4tfnM_WnQU",
                    "content-encoding": "utf-8",
                }
                mosru_fullname = f"{data.get('first_name')} {data.get('last_name')} {data.get('username')}"
                print(r.text)
                usr = Account.objects.get(pk=request.user.pk)
                request.session['token'] = data.get('authentication_token')
                usr.token = data.get('authentication_token')
                usr.save()
    else:
        form = LinkingMosruForm()
    return render(request, "linking_mosru.html", {"form": form, "linked": False})


def choice(request):
    school_number = str(SchoolInfo.objects.all().first().number)
    active_types = {
        "organizer": [{
            "name": "Организатор",
            "description": "Просмотр и редактирование своих мероприятий",
            "url": "/lk/organizer",
            "in_dev": False,
            "image": "organizer"
        }, Events.objects.all().filter(organizer=request.user).exists()],
        "statistics": [{"name": "Статистика", "description": f"Статистика КА ГБОУ Школы {school_number}", "in_dev": True,
                        "url": "/lk/statistics", "image": "statistics"}, request.user.is_developer],
        "developer": [
            {"name": "Разработчик", "description": "Логи, Тех-поддержка", "in_dev": False, "url": "/lk/developer",
             "image": "developer"}, request.user.is_developer],
        "methodist": [{"name": "Методист", "description": f"Методист ГБОУ Школы {school_number}", "in_dev": True,
                       "url": "/lk/methodist", "image": "methodist"}, request.user.has_role("methodist")],
        "admin": [{"name": "Администрация", "description": f"Администратор ГБОУ Школы {school_number}", "in_dev": False,
                   "url": "/lk/admin", "image": "admin"}, request.user.has_roles(["admin", "director"])],
        "teacher": [{"name": "Преподаватель", "description": f"Преподаватель ГБОУ Школы {school_number}", "in_dev": False,
                     "url": "/lk/teacher", "image": "teacher"}, request.user.has_role("teacher")],
        "psychologist": [{"name": "Психолог", "description": f"Психолог ГБОУ Школы {school_number}", "in_dev": False,
                          "url": "/lk/psychologist", "image": "psychologist"}, request.user.has_role("psychologist")],

    }

    tmp = {}

    for i in active_types:
        if active_types[i][1]:
            tmp[i] = active_types[i][0]
            if active_types[i][0]["in_dev"]:
                if not request.user.is_developer:
                    tmp[i]["name"] = "Скоро..."
                    tmp[i]["description"] = "В разработке"
                    tmp[i]["url"] = "#"
                    tmp[i]["image"] = "dev"
                else:
                    tmp[i]['name'] = tmp[i]['name'] + " (в разработке)"

    return render(request, "choice.html", {"active_types": tmp})
