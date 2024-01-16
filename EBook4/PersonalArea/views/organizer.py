from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from Accounts import decorators
from MainApp.models import Events, Materials, OrganizationScenario
from PersonalArea.forms import AddMaterialForm


def index(request):
    return render(request, "organizer/index.html")


def events(request):
    events = Events.objects.all().filter(organizer=request.user, end_date__gt=timezone.now()).order_by("-start_date")
    return render(request, "organizer/events.html", {"events": events})

def materials(request,event_id):
    event = Events.objects.get(pk=event_id)
    if request.method == "POST":
        files = request.FILES.getlist("file")

        for f in files:
            m = Materials(name=f.name, file=f)
            m.save()
            event.organizer_materials.add(m)
        event.save()
        return redirect(f"/lk/organizer/events/{event_id}/materials")

    else:
        form = AddMaterialForm()
        m = event.organizer_materials.all()
        return render(request, "organizer/materials.html", {"materials": m, "form": form})


def edit_event_scenario(request, event_id):
    if request.method == "POST":
        text = request.POST.get("text")
        print(text)
        if text is not None:
            event = Events.objects.get(pk=event_id, organizer=request.user)
            r = OrganizationScenario.objects.create(name=text)
            r.save()
            event.organizer_scenario.add(r)
            event.save()
        return redirect(f"/lk/organizer/events/{event_id}/edit")
    else:
        event = Events.objects.get(pk=event_id, organizer=request.user)
        return render(request, "organizer/edit.html", {"scenario": event.organizer_scenario.all().order_by("id")})

def view_event_scenario(request, event_id):
    event = Events.objects.get(pk=event_id, organizer=request.user)
    return render(request, "organizer/view.html", {"scenario": event.organizer_scenario.all().order_by("id"),
                                                   "members": event.volunteer.all().order_by("user__second_name")})
