from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
urlpatterns = [
    path("roles/", views.setup_roles_view),
    path("account/create/", views.account),
    path("school/settings", views.settings),
    path("",views.index)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
