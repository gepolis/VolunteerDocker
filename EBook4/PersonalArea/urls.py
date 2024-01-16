from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

from . import views

urls1 = [
    path("", views.other.index),
    path("choice/", views.other.choice),
    path("chat/", views.other.chat),


    path("events/<int:id>/detail/", views.other.event_detail),
    path("events/category/data/<int:id>/", views.admin.category_data),
    path("events/invites/", views.student.student_invites),
    path("events/all_events/", views.other.all_events),

    path("building/list/", views.admin.building_list),
    path("building/add/", views.admin.add_building),
    path("events/list/<str:search>/", views.aam.events_list),
    path("events/archive/", views.aam.events_archive_list),
    path('settings/', views.other.edit_profile),
    path("events/create/", views.aam.event_create),
    path("events/", views.other.events),


    path("events/<int:event>/request/", views.student.event_request),
    path("my/events/", views.student.my_events),

    path("classrooms/", views.administration.classrooms_list, name="classrooms_list"),
    path("classrooms/<int:id>", views.administration.classrooms_view, name="classrooms_view"),
    path("settings/avatar/remove/", views.other.avatar_remove, name="avatar_remove"),

    path("settings/security/change-password/", views.other.change_password, name="change_password"),
    path("settings/security/devices/", views.other.devices, name="security"),
    path("settings/security/devices/delete/<str:device>/", views.other.delete_device, name="delete_device"),
    path("settings/linking/mosru/", views.other.settings_linking_mosru, name="settings_linking_mosru"),

    path("developer/", views.developer.developer),
    path("developer/feedbacks/", views.developer.feedbacks, name="feedbacks"),
    path("developer/feedbacks/archive/", views.developer.feedbacks_archive, name="feedbacks_archived"),
    path("developer/feedbacks/<int:fb_id>/", views.developer.view_feedback, name="view_feedback"),
    path("developer/feedbacks/<int:fb_id>/send/", views.developer.send_feedback_answer, name="send_feedback_answer"),
    path("developer/logs/", views.developer.get_logs, name="logs"),
    path("developer/drag/", views.developer.drag, name="drag"),


    path("personalisation/locations", views.personalisation.locations, name="personalisation"),
    path("personalisation/location/<int:id>", views.personalisation.location, name="location"),
# path("classroom/student/<int:user>/delete", views.classroom_delete_student),
]


urls_with_not_slash = [
    path("chat/", views.other.chat),

    path("classroom/students/pdf", views.teacher.students_list2pdf),



    path("events/<int:id>/detail", views.other.event_detail),



    path("events/list/<str:search>", views.aam.events_list),
    path("events/archive", views.aam.events_archive_list),
    path("events/create", views.aam.event_create),
    path("events/<int:id>/photo/report/<int:image>/delete", views.aam.photo_delete),

    path("events/<int:event>/request", views.student.event_request),
    path("my/events", views.student.my_events),
    path("events/invites", views.student.student_invites),
    path("events/all_events", views.other.all_events),

    path("personalisation/locations", views.personalisation.locations, name="personalisation"),
    path("personalisation/location/<int:id>", views.personalisation.location, name="location"),
]

organizer_urls = [
    path("organizer", views.organizer.index, name="organizer"),
    path("organizer/events", views.organizer.events, name="organizer_events"),
    path("organizer/events/<int:event_id>/materials", views.organizer.materials, name="organizer_event_detail"),
    path("organizer/events/<int:event_id>/edit", views.organizer.edit_event_scenario, name="organizer_event_detail"),
    path("organizer/events/<int:event_id>/view", views.organizer.view_event_scenario, name="organizer_event_view"),

]

admin_stats_urls = [
    path("statistics/", views.statistics.index, name="admin_stats"),

]


teacher_urls = [
    path("teacher/classroom/create/", views.teacher.create_classroom),
    path("teacher/events/", views.other.events),
    path("teacher/events/<int:id>/invite/", views.teacher.invite_classroom_event),
    path("teacher/classroom/invite/create/", views.teacher.create_invite),
    path("teacher/classroom/invite/update/", views.teacher.update_invite),
    path("teacher/classroom/invite/<uuid:classroom>/", views.student.invite),
    path("teacher/classroom/students/", views.teacher.classroom_students),
    path("teacher/", views.teacher.index),
    path("teacher/classroom/student/<int:user>/view/", views.teacher.classroom_view_student),
    path("teacher/classroom/student/<int:user>/export/", views.other.classroom_view_export),

    path("teacher/classroom/create", views.teacher.create_classroom),
    path("teacher/events", views.other.events),
    path("teacher/events/<int:id>/invite", views.teacher.invite_classroom_event),
    path("teacher/classroom/invite/create", views.teacher.create_invite),
    path("teacher/classroom/invite/update", views.teacher.update_invite),
    path("teacher/classroom/invite/<uuid:classroom>", views.student.invite),
    path("teacher/classroom/students", views.teacher.classroom_students),
    path("teacher", views.teacher.index),
    path("teacher/classroom/student/<int:user>/view", views.teacher.classroom_view_student),
    path("teacher/classroom/student/<int:user>/export", views.other.classroom_view_export),
    path("classroom/students/upload/", views.teacher.classroom_students_upload),
    path("classroom/students/pdf/", views.teacher.students_list2pdf),

]
psychologist_urls = [
    path('psychologist/schedule', views.psychologist.schedule_index, name="schedule_index"),
    path('psychologist/schedule/add', views.psychologist.schedule_add, name="schedule_add"),
    path('psychologist/schedule/<int:d>/<int:m>/<int:y>', views.psychologist.schedule_date, name="schedule_date"),
    path('psychologist/schedule/calendar', views.psychologist.calendar, name="calendar"),
    path('psychologist/schedule/edit', views.psychologist.edit_schedule, name="edit_schedule"),
    path('psychologist/schedule/has_month_classes/<int:m>/<int:y>', views.psychologist.has_month_classes, name="has_month_classes"),
    path('psychologist/schedule/view/<int:id>', views.psychologist.view_schedule, name="view_schedule"),
    path('psychologist/classes', views.psychologist.classes, name="classes"),

    path('psychologist/schedule/', views.psychologist.schedule_index, name="schedule_index"),
    path('psychologist/schedule/add/', views.psychologist.schedule_add, name="schedule_add"),
    path('psychologist/schedule/<int:d>/<int:m>/<int:y>/', views.psychologist.schedule_date, name="schedule_date"),
    path('psychologist/schedule/calendar/', views.psychologist.calendar, name="calendar"),
    path('psychologist/schedule/edit/', views.psychologist.edit_schedule, name="edit_schedule"),
    path('psychologist/schedule/has_month_classes/<int:m>/<int:y>/', views.psychologist.has_month_classes, name="has_month_classes"),
    path('psychologist/schedule/view/<int:id>/', views.psychologist.view_schedule, name="view_schedule"),
    path('psychologist/classes/', views.psychologist.classes, name="classes"),

    path('psychologist/', views.psychologist.index),
    path('psychologist', views.psychologist.index),
]

admin_urls = [
    path("admin/users/list", views.administration.users_list),
    path("admin/users/list/<str:role>", views.administration.users_list),
    path("admin/users/create", views.admin.user_create, name="create_user"),
    path("admin/users/<int:id>/edit", views.administration.edit_user),
    path("admin/users/<int:id>/delete", views.admin.user_delete),
    path("admin/users/data/<int:id>", views.administration.user_data),
    path("admin/users/<int:id>/view", views.administration.view_user),
    path("admin/users/<int:user>/login", views.admin.login_admin_user),
    path("admin/users/<int:user>/avatar/remove", views.administration.avatar_remove),
    path("admin/events/<int:id>/view", views.aam.events_view),
    path("admin/events/category/list", views.admin.category_list, name="category_list"),
    path("admin/events/category/<int:id>/edit", views.admin.category_edit),
    path("admin/events/<int:id>/accept/<int:user>", views.aam.event_accept_user),
    path("admin/events/<int:id>/reject/<int:user>", views.aam.event_reject_user),
    path("admin/events/<int:id>/add/<int:user>", views.admin.event_add_user),
    path("admin/events/<int:id>/export", views.aam.event_export),
    path("admin/events/<int:id>/unarchived", views.aam.event_unarchived),
    path("admin/events/<int:id>/archive", views.aam.event_archive),
    path("admin/events/<int:id>/points/give", views.aam.give_points),
    path("admin/events/<int:id>/photo/report", views.aam.photo_report),
    path("admin/users/list/", views.administration.users_list),
    path("admin/users/list/<str:role>/", views.administration.users_list),
    path("admin/users/create/", views.admin.user_create, name="create_user"),
    path("admin/users/<int:id>/edit/", views.administration.edit_user),
    path("admin/users/<int:id>/delete/", views.admin.user_delete),
    path("admin/users/data/<int:id>/", views.administration.user_data),
    path("admin/users/<int:id>/view/", views.administration.view_user),
    path("admin/users/<int:user>/login/", views.admin.login_admin_user),
    path("admin/users/<int:user>/avatar/remove/", views.administration.avatar_remove),
    path("admin/events/<int:id>/view/", views.aam.events_view),
    path("admin/events/category/list/", views.admin.category_list, name="category_list"),
    path("admin/events/category/<int:id>/edit/", views.admin.category_edit),
    path("admin/events/<int:id>/accept/<int:user>/", views.aam.event_accept_user),
    path("admin/events/<int:id>/reject/<int:user>/", views.aam.event_reject_user),
    path("admin/events/<int:id>/add/<int:user>/", views.admin.event_add_user),
    path("admin/events/<int:id>/export/", views.aam.event_export),
    path("admin/events/<int:id>/unarchived/", views.aam.event_unarchived),
    path("admin/events/<int:id>/archive/", views.aam.event_archive),
    path("admin/events/<int:id>/points/give/", views.aam.give_points),
    path("admin/events/<int:id>/photo/report/", views.aam.photo_report),
    path("admin/classrooms/", views.administration.classrooms_list, name="classrooms_list"),
    path("admin/classrooms/<int:id>/", views.administration.classrooms_view, name="classrooms_view"),
    path("admin/classrooms", views.administration.classrooms_list, name="classrooms_list"),
    path("admin/classrooms/<int:id>", views.administration.classrooms_view, name="classrooms_view"),
    path("admin/events/<int:id>/photo/report/<int:image>/delete/", views.aam.photo_delete),
    path("admin/", views.admin.index),
    path("admin", views.admin.index),
    path("admin/events/category/data/<int:id>", views.admin.category_data),
    path("admin/building/list", views.admin.building_list),
    path("admin/building/add", views.admin.add_building),
    path("admin/events/category/data/<int:id>/", views.admin.category_data),
    path("admin/building/list/", views.admin.building_list),
    path("admin/building/add/", views.admin.add_building),
]

developer_urls = [
    path("developer", views.developer.developer),
    path("developer/feedbacks", views.developer.feedbacks, name="feedbacks"),
    path("developer/feedbacks/archive", views.developer.feedbacks_archive, name="feedbacks_archived"),
    path("developer/feedbacks/<int:fb_id>", views.developer.view_feedback, name="view_feedback"),
    path("developer/feedbacks/<int:fb_id>/send", views.developer.send_feedback_answer, name="send_feedback_answer"),
    path("developer/logs", views.developer.get_logs, name="logs"),
    path("developer/drag", views.developer.drag, name="drag"),
    path("developer/", views.developer.developer),

    path("developer/feedbacks/", views.developer.feedbacks, name="feedbacks"),
    path("developer/feedbacks/archive/", views.developer.feedbacks_archive, name="feedbacks_archived"),
    path("developer/feedbacks/<int:fb_id>/", views.developer.view_feedback, name="view_feedback"),
    path("developer/feedbacks/<int:fb_id>/send/", views.developer.send_feedback_answer, name="send_feedback_answer"),
    path("developer/logs/", views.developer.get_logs, name="logs"),
    path("developer/drag/", views.developer.drag, name="drag"),

]
settings_urls = [
    path("settings/avatar/remove", views.other.avatar_remove, name="avatar_remove"),
    path('settings', views.other.edit_profile),
    path("settings/security/change-password", views.other.change_password, name="change_password"),
    path("settings/security/devices", views.other.devices, name="security"),
    path("settings/security/devices/delete/<str:device>", views.other.delete_device, name="delete_device"),
    path("settings/linking/mosru", views.other.settings_linking_mosru, name="settings_linking_mosru"),

]

student_urls = [
    path("events/<int:event>/request", views.student.event_request),
    path("my/events", views.student.my_events),
    path("events/invites", views.student.student_invites),
    path("events/<int:event>/request/", views.student.event_request),
    path("my/events/", views.student.my_events),
    path("events/invites/", views.student.student_invites),
]


print(len(teacher_urls))
urlpatterns = (
        (urls1 + urls_with_not_slash) +
        (psychologist_urls + teacher_urls + admin_stats_urls + admin_urls + developer_urls + student_urls) +
        settings_urls +
        organizer_urls +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))