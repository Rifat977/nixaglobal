from django.urls import path
from . import views

app_name="core"
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('all_agent/', views.all_agent, name="all_agent"),
    path('my_agents/', views.my_agents, name="my_agents"),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
    path('profile_manage/<int:pk>', views.profile_manage, name="profile_manage"),

    path('commission_tier/', views.commission_tier, name="commission_tier"),
    path('comission_manage/<int:pk>', views.comission_manage, name="comission_manage"),

    path('university/', views.university, name="university"),
    path('university/delete/<int:pk>', views.university_delete, name="university_delete"),
    path('university/edit/', views.university_edit, name="university_edit"),

    path('university/details/<int:pk>', views.university_details, name="university_details"),

    path('application/', views.application, name="application"),
    path('application/status/<int:pk>', views.application_status, name="application_status"),

    path('admin-application/', views.admin_application, name="admin_application"),
    path('admin-manage-status/<int:pk>', views.admin_manage_status, name="admin_manage_status"),

    path('payment_request/', views.payment_request, name="payment_request"),

    path('admin-manage-requests/<int:pk>', views.admin_manage_requests, name="admin_manage_requests"),

    path('agent_applications/<int:pk>', views.agent_applications, name="agent_applications"),
]