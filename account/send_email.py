from django.core.mail import send_mail
from .models import CustomUser

def send_email(subject, message, user):
    send_mail(subject, message, 'sender@example.com', [user.email])

def send_email_to_admin(subject, message):
    admins = CustomUser.objects.filter(user_type='Admin')
    for admin in admins:
        send_mail(subject, message, 'sender@example.com', [admin.email])