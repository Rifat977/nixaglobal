from django.urls import path
from . import views

app_name="core"
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
    path('profile_manage/<int:pk>', views.profile_manage, name="profile_manage"),
]