from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token
from MainApp.models import *
def get_user_by_token(request):
    t = request.META.get('HTTP_AUTHORIZATION')
    if t:
        return Token.objects.get(key=t.split()[1]).user
    return None
class IsAdmin(BasePermission):
    message = "Access Denied!"
    def has_permission(self, request, view):
        user = get_user_by_token(request)
        if user:
            if user.has_role("admin") or user.has_role("director") or user.has_role("head_teacher"):
                return True
        return False


    def has_object_permission(self, request, view, obj):
        user = get_user_by_token(request)
        if user:
            if request.type == 'POST':

                if user.is_superuser:
                    return True
                if user == obj.member:
                    return True
                return False
            if request.type == 'DELETE':
                if user.is_superuser:
                    return True
                if request.user == obj.member:
                    return True
                return False
            if request.type == 'GET':
                return True
        return False


class IsStaff(BasePermission):
    message = "Access Denied!"
    def has_permission(self, request, view):
        user = get_user_by_token(request)
        if user:
            if user.has_role("admin") or user.has_role("director") or user.has_role("head_teacher") or user.has_role("methodist") or user.has_role("teacher") or user.has_role("psychologist"):
                return True
        return False


    def has_object_permission(self, request, view, obj):
        user = get_user_by_token(request)
        if user:
            if user.has_role("admin") or user.has_role("director") or user.has_role("head_teacher") or user.has_role("methodist") or user.has_role("teacher") or user.has_role("psychologist"):
                return True
        return False