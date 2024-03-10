from django.urls import path
from . import views

app_name="core"
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('all_agent/', views.all_agent, name="all_agent"),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
    path('profile_manage/<int:pk>', views.profile_manage, name="profile_manage"),
    path('comission_manage/<int:pk>', views.comission_manage, name="comission_manage"),

    path('university/', views.university, name="university"),
    path('university/delete/<int:pk>', views.university_delete, name="university_delete"),
    path('university/edit/', views.university_edit, name="university_edit"),

    path('application/', views.application, name="application"),


]