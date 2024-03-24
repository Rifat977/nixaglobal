from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('register/', views.register, name="register"),

    path('new-password/<uidb64>/<token>/', views.new_password, name='new_password'),
    path('forgot_password/', views.forgot_password, name="forgot_password"),

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout, name='logout'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
]