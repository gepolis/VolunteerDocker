import math

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from Accounts.models import Account, Building
from MainApp.models import Events, EventsMembers, EventCategory, ClassRoom
from rest_framework import generics, mixins
from rest_framework import permissions
from .serializers import *
from .permissions import IsAdmin, IsStaff


def pagination_queryset(request, queryset, items_per_page=25):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    offset = (page - 1) * items_per_page
    limit = items_per_page + offset
    queryset = queryset.order_by('-id')


    max_page = math.ceil(queryset.count() / items_per_page)
    if len(request.GET) >= 1 and not request.GET.get("page"):
        arg_char = "&"
    else:
        arg_char = "?"

    if page > 1:
        prev = f"{arg_char}page=" + str(page - 1)
    else:
        prev = None
    if page < max_page:
        next = f"{arg_char}page=" + str(page + 1)
    else:
        next = None
    queryset = queryset[offset:limit]
    return max_page, queryset, page,prev, next

class BuildingViewSet(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        buildings = BuildingSerializer(Building.objects.all(), many=True)
        return Response({"results":buildings.data})

class EventsViewSet(APIView):
    permission_classes = [IsStaff]

    @action(methods=['get'], detail=False)
    def get(self, request):
        queryset = Events.objects.all()
        token = request.META.get('HTTP_AUTHORIZATION')

        if token:
            user = Token.objects.get(key=token.split()[1]).user
        if request.user.role == "methodist":
            categories = EventCategory.objects.all().filter(methodists=user)
            queryset = queryset.filter(category__in=categories)
        elif request.user.role == "head_teacher":
            queryset = queryset.filter(building=user.building)
        if request.GET.get('archive'):
            queryset = queryset.filter(archive=True).order_by("-id")
        else:
            queryset = queryset.filter(archive=False).order_by("-id")
        max_page, queryset, page,prev, next = pagination_queryset(request, queryset)
        serializer = EventsSerializer(queryset, many=True)
        return Response(
            {"results": serializer.data, "prev": prev, "next": next, "max": max_page, "page": page})


class ProfileViewSet(APIView):
    def get(self, request, pk=None):
        if pk is None:
            token = request.META.get('HTTP_AUTHORIZATION')
            if token:
                user = Token.objects.get(key=token.split()[1]).user
            pk = user.id
        queryset = Account.objects.get(pk=pk)
        serializer = ProfileSerializer(queryset)
        events = Events.objects.filter(volunteer__user=queryset)
        e = EventsSerializer(events, many=True)

        return Response({"user": serializer.data, "events": e.data})


class UsersViewSet(APIView):
    permission_classes = [IsAdmin]

    @action(methods=['get'], detail=False)
    def get(self, request):
        queryset = Account.objects.all().filter(is_superuser=False)
        token = request.META.get('HTTP_AUTHORIZATION')

        if token:
            user = Token.objects.get(key=token.split()[1]).user
        if user.has_role("head_teacher") and not request.user.has_roles(["admin", "director"]):
            queryset = queryset.filter(building_id=user.building_id)
        max_page, q, page,prev, next = pagination_queryset(request, queryset)
        serializer = UsersSerializer(q, many=True)
        statictic = {
            "staff": queryset.filter((Q(role__label="methodist") | Q(role__label="head_teacher") | Q(role__label="admin") | Q(role__label="teacher") | Q(role__label="director") | Q(role__label="psychologist")) & Q(is_superuser=False)).count(),
            "parents": 0,
            "students": queryset.filter(role__label="student").count(),
            "all": queryset.count(),

        }
        return Response(
            {"results": serializer.data, "prev": prev, "next": next, "max": max_page, "page": page, "statictic": statictic})



class ClassroomsViewSet(APIView):
    permission_classes = [IsAdmin]

    @action(methods=['get'], detail=False)
    def get(self, request):
        queryset = ClassRoom.objects.all()
        token = request.META.get('HTTP_AUTHORIZATION')
        max_page, queryset, page,prev, next = pagination_queryset(request, queryset)
        serializer = ClassroomSerializer(queryset, many=True)
        return Response(
            {"results": serializer.data, "prev": prev, "next": next, "max": max_page, "page": page})
