from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import *
from account.models import *
from django.contrib import auth, messages

# Create your views here.
def index(request):
    return render(request, 'guest/index.html')

@login_required
@any_user_required
def dashboard(request):
    user = request.user
    if user.is_admin:
        pending_agents = CustomUser.objects.filter(is_active=False)
        context = {
            'user_type': UserType.ADMIN,
            'pending_agents': pending_agents
        }
    elif user.is_agent:
        context = {
            'user_type': UserType.AGENT,
        }
    elif user.is_sub_agent:
        context = {
            'user_type': UserType.SUB_AGENT,
        }
    elif user.is_exclusive_agent:
        context = {
            'user_type': UserType.EXCLUSIVE_AGENT,
        }
    return render(request, 'portal/dashboard.html', context)

@login_required
def profile_settings(request):
    user = request.user

    if request.method == 'POST':
        # profession = request.POST.get('profession')
        # company_name = request.POST.get('company_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        post_code = request.POST.get('post_code')
        avatar = request.FILES.get('avatar')

        errors = {}

        if not first_name:
            errors['first_name'] = 'First name is required.'

        if not last_name:
            errors['last_name'] = 'Last name is required.'

        if old_password and (not new_password or not confirm_password):
            errors['password'] = 'New password and confirm password are required when changing password.'
        elif old_password and new_password != confirm_password:
            errors['password'] = 'New password and confirm password do not match.'
        elif old_password and not request.user.check_password(old_password):
            errors['password'] = 'Old password is incorrect.'


        if avatar and not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            errors['avatar'] = 'Avatar must be an image file (JPG, JPEG, PNG, GIF).'

        if errors:
            for field, error_message in errors.items():
                messages.error(request, error_message)
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.address = address
            user.country = country
            user.city = city
            user.post_code = post_code
            if new_password:
                user.set_password(new_password)
            if avatar:
                user.avatar = avatar


            user.save()
            messages.success(request, 'Profile updated successfully.')

        return redirect('core:profile_settings')
    return render(request, 'portal/profile_settings.html', {'user':user})

@login_required
@admin_required
def profile_manage(request, pk):
    user = CustomUser.objects.get(pk=pk)
    documents = DocumentImage.objects.filter(identification_document__user=user)
    try:
        company = Company.objects.get(user=user)
        trade_license = company.trade_license
        print(trade_license)
    except Company.DoesNotExist:
        trade_license = None
    if request.method == 'POST':
        post_code = request.POST.get('post_code')
        is_verified = request.POST.get('is_verified')
        is_active = request.POST.get('is_active')

        if is_verified == 'on':
            is_verified = True
        else:
            is_verified = False

        if is_active == 'on':
            is_active = True
        else:
            is_active = False

        errors = {}

        if errors:
            for field, error_message in errors.items():
                messages.error(request, error_message)
        else:
            user.is_active = is_active
            user.is_verified = is_verified
            user.save()
            messages.success(request, 'Profile updated successfully.')
    return render(request, 'portal/profile_manage.html', {'user':user, 'documents': documents, 'trade_license': trade_license})