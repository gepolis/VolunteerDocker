
import threading
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from MainApp.models import *

from PersonalArea.forms import *
from Accounts import decorators
@decorators.is_teacher
def create_classroom(request):
    if ClassRoom.objects.all().filter(teacher=request.user).exists():
        return redirect("/lk/")
    if request.method == "GET":
        form = NewClassRoom()
    else:
        form = NewClassRoom(request.POST)
        if form.is_valid():
            if form.unique():
                classroom = form.save(commit=False)
                classroom.teacher = request.user
                classroom.save()
            else:
                classroom = ClassRoom.objects.get(classroom=int(request.POST["classroom"]),parallel=str(request.POST["parallel"]).upper())
                if classroom.teacher is None:
                    classroom.teacher = request.user
                    classroom.save()
                    messages.success(request,
                                     "Вы успешно получили доступ к классу.")
                else:
                    messages.error(request,
                                   "Данный класс уже существует. Если вы являетесь классным руководителем класса который уже существует, обратитесь к администрации.")
                return render(request, "teacher/create_classroom.html", {"form": form, "section": "classroom"})
        return redirect("/lk/")
    return render(request, "teacher/create_classroom.html", {"form": form, "section": "classroom"})


@decorators.is_teacher
def create_invite(request):
    if ClassRoom.objects.all().filter(teacher=request.user).exists():
        classroom = ClassRoom.objects.get(teacher=request.user)
        return render(request, "teacher/invite.html", {"uuid": classroom.uuid, "section": "classroom"})
    else:
        return redirect("/lk/classroom/create/")


@decorators.is_teacher
def update_invite(request):
    if ClassRoom.objects.all().filter(teacher=request.user).exists():
        classroom = ClassRoom.objects.get(teacher=request.user)
        classroom.uuid = uuid.uuid4()
        classroom.save()
        return redirect("/lk/classroom/invite/create/")
    else:
        return redirect("/lk/classroom/create/")


@decorators.is_teacher
def invite_classroom_event(request, id):
    if ClassRoom.objects.all().filter(teacher=request.user).exists():
        classroom = ClassRoom.objects.get(teacher=request.user)
        event = Events.objects.get(pk=id)
        for member in classroom.member.all():
            if not event.volunteer.all().filter(user=member).exists():
                vol = EventsMembers.objects.create(user=member, is_active=True)
                event.volunteer.add(vol)
        messages.success(request, "Вы успешно пригласили класс на мероприятие.")
        return redirect("/lk/events/")
    else:
        return redirect("/lk/classroom/create/")


@decorators.is_teacher
def classroom_students(request):
    if ClassRoom.objects.all().filter(teacher=request.user).exists():
        classroom = ClassRoom.objects.get(teacher=request.user)
        members = classroom.member.all()
        return render(request, "teacher/students.html", {"members": members, "section": "classroom"})
    else:
        return redirect("/lk/classroom/create/")


@decorators.is_teacher
def classroom_view_student(request, user):
    if ClassRoom.objects.all().filter(teacher=request.user).exists():
        classroom = ClassRoom.objects.get(teacher=request.user)
        if classroom.member.all().filter(pk=user).exists():
            user = classroom.member.get(pk=user)
            events = Events.objects.all().filter(volunteer__user=user)
            return render(request, "teacher/view_student.html",
                          {"student": user, "events": events, "section": "classroom"})
        else:
            return redirect("/lk/classroom/students/")
    else:
        return redirect("/lk/classroom/create/")

@decorators.is_teacher
def classroom_students_upload(request):
    if request.method == "POST":
        t = threading.Thread(target=students_upload_thr, args=(request,))
        t.start()
        messages.success(request, "Начинаю загрузку, пожалуйста, подождите!")
        red = redirect("/lk/classroom/students/")
        return red
    else:
        return render(request, "teacher/students_upload.html", {"section": "classroom"})

def students_upload_thr(request):
    file = request.FILES["file"]
    file_lines = file.read().decode("utf-8").splitlines()
    class_room = ClassRoom.objects.get(teacher=request.user)
    try:
        for row in file_lines:
            print(row)
            d = row.split(" ")
            sn, fn, mn = d[0], d[1], d[2]

            if not Account.objects.filter(first_name=fn, middle_name=mn, second_name=sn,
                                          account__classroom=class_room).exists():
                usr = Account.objects.create(first_name=fn, middle_name=mn, second_name=sn, role="student")
                usr.building = request.user.building

                random_word = ['венок', 'забава', 'прыгун', 'флажок', 'свет', 'арена', 'цвет', 'стиль', 'роза']
                word = random.choice(random_word)
                random_number = random.randint(1000, 9999)
                first_number = random.randint(0, 1)
                if first_number == 0:
                    password = word + str(random_number)
                else:
                    password = str(random_number) + word
                usr.set_password(password)
                usr.username = f"student_{usr.id}"
                usr.save()
                class_room.member.add(usr)
                clu = ClassRoomTeacherAuthUser.objects.create(user=usr, classroom=class_room, password=password)
                clu.save()
    except Exception as e:
        print("Error")
        print(e)
        messages.error(request, "Что-то пошло не так!")

    messages.success(request, "Загрузка завершена!")
    request.COOKIES["lif"] = 0

@decorators.is_teacher
def students_list2pdf(request):
    if ClassRoom.objects.all().filter(teacher=request.user).exists():
        classroom = ClassRoom.objects.get(teacher=request.user)
        members = ClassRoomTeacherAuthUser.objects.all().filter(classroom=classroom)
        return render(request, "teacher/students_pdf.html", {"members": members, "section": "classroom", "classroom": classroom})
    else:
        return redirect("/lk/classroom/create/")

@decorators.is_teacher
def index(request):
    return render(request, "teacher/index.html", {"section": "index"})