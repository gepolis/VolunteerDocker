from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from Accounts import views as accounts_views
from MainApp import views
from SetupApp import views as setup_views
from rest_framework.authtoken import views as rest_framework_views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('register/<str:mode>/', accounts_views.register),
                  path('login/', accounts_views.login_request),
                  path('logout/', accounts_views.logout_request, name="logout"),

                  path('lk/', include("PersonalArea.urls")),
                  path('setup/', include("SetupApp.urls")),
                  path('', views.index),
                  path('auth/', accounts_views.auth, name="auth"),
                  path('auth/mosru/', accounts_views.auth_mos_ru, name="auth"),
                  path('auth/mosru/status/<str:uuid>/', accounts_views.mos_ru_status, name="auth_status"),
                  path('auth/mosru/login/<str:uuid>/', accounts_views.mos_ru_login, name="auth_login"),
                  path('auth/mosru/info/', accounts_views.mos_ru_info, name="auth"),
                  path('auth/register', accounts_views.register_request),
                  path('auth/login', accounts_views.login_request),
                  path('chatbot/', include("ChatBot.urls")),
                  path("user_activity/", accounts_views.user_activity),
                  path("feedback/", views.feedback),
                  path('api/', include('api.urls')),
                  path('api-token-auth/', rest_framework_views.obtain_auth_token, name='api-token-auth'),
                  path('token', views.token),
                  #path("__debug__/", include("debug_toolbar.urls")),
                  path(
                      "robots.txt",
                      TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
                  ),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


def handler404(request, *args, **argv):
    return render(request, 'errors/404.html', status=404)


def handler500(request, *args, **argv):
    return render(request, 'errors/500.html', status=500)


def handler403(request, *args, **argv):
    return render(request, 'errors/403.html', status=403)


handler403 = handler403
handler500 = handler500
handler404 = handler404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
