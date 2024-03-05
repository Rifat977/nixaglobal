from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
]