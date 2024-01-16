from django.urls import path
from .views import *


urlpatterns = [
    path(r'events/', EventsViewSet.as_view()),
    path(r'users/', UsersViewSet.as_view()),
    path(r'profile/', ProfileViewSet.as_view()),
    path(r'profile/<int:pk>', ProfileViewSet.as_view()),
    path(r'buildings/', BuildingViewSet.as_view()),
    path(r'classrooms/', ClassroomsViewSet.as_view()),
]