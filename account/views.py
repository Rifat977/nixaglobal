from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import *
from django.contrib import auth, messages
from django.core.files.uploadedfile import UploadedFile

import random, string

from django.core.mail import send_mail
from django.utils.crypto import get_random_string, constant_time_compare
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

User = get_user_model()
DOMAIN_NAME = "http://127.0.0.1:8000"

# Create your views here.
def generate_referral_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(10))

def send_verification_email(user):
    subject = 'Verify your email address'
    token = user.email_verification_token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"{DOMAIN_NAME}/account/verify-email/{uid}/{token}/"
    message = f'Click the following link to verify your email address: {verification_url}'
    send_mail(subject, message, 'sender@example.com', [user.email])

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if user.is_verified:
                messages.success(request, 'Email already verified.')
            else:
                user.is_verified = True
                user.save()
                messages.success(request, 'Email verified successfully.')
            return redirect('core:index')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('account:register')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('account:register')

def register(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        trade_license = request.FILES.get('trade_license')

        account_type = request.POST.get('account_type')
        profession = request.POST.get('profession')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        post_code = request.POST.get('post_code')
        document_type = request.POST.get('document_type')
        identification_documents = request.FILES.getlist('identification_document')

        errors = []

        if account_type == 'Individual' and not profession:
            errors.append('Profession is required for Individual account.')

        if account_type == 'Company':
            if not company_name:
                errors.append('Company name is required for company account.')
            if not trade_license:
                errors.append('Trade License is required for company account.')

        if User.objects.filter(email=email).exists():
            errors.append('Email already exists. Please use a different email address.')

        required_fields = {
            'First Name': first_name,
            'Last Name': last_name,
            'Email': email,
            'Phone Number': phone_number,
            'Password': password,
            'Confirm Password': confirm_password,
            'Address': address,
            'Country': country,
            'City': city,
            'Post Code': post_code,
            'Document Type': document_type,
            'Identification Document': identification_documents
        }
        
        missing_fields = [field for field, value in required_fields.items() if value is None or value == '']
        if missing_fields:
            errors.append("The following fields are required: {}".format(', '.join(missing_fields)))

        if password != confirm_password:
            errors.append('Password and Confirm Password do not match.')

        if errors:
            for error_message in errors:
                messages.error(request, error_message)
            return render(request, 'guest/register.html')

        referral_code = generate_referral_code()

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            referral_code=referral_code,
            company_name=company_name,
            profession=profession,
            account_type=account_type,
            is_active=False
        )

        if account_type == 'Company':
            company = Company.objects.create(
                user=user,
                trade_license=trade_license
            )

        token = default_token_generator.make_token(user)
        user.email_verification_token = token
        user.email_verification_sent_at = timezone.now()
        user.phone_number = phone_number
        user.address = address
        user.country = country
        user.city = city
        user.post_code = post_code
        user.save()

        for file in identification_documents:
            document = IdentificationDocument.objects.create(
                user=user,
                document_type=document_type,
            )
            DocumentImage.objects.create(identification_document=document, image=file)

        send_verification_email(user)

        messages.success(request, 'Account created successfully, waiting for admin approval')
        
    return render(request, 'guest/register.html')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email')
        password = request.POST.get('password')

        if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
                identifier = user.username

        user = authenticate(request, username=identifier, password=password)
        print(user)
        if user is not None:
            if user.is_verified:
                if user.is_active:
                    print("hello")
                    login(request, user)
                    return redirect('core:dashboard')
                else:
                    messages.error(request, 'Your account is inactive. Please contact the administrator.')
            else:
                messages.error(request, 'Your account is unverified. Please verify your account.')
        else:
            messages.error(request, 'Invalid username, email, or password.')

    return redirect('core:index')


@login_required
def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('account:login')