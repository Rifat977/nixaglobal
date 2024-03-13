from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import *
from account.models import *
from django.contrib import auth, messages
from .models import *
from decimal import Decimal
from django.core.validators import DecimalValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ObjectDoesNotExist

import string, random

# Create your views here.
def index(request):
    return render(request, 'guest/index.html')

@login_required
@any_user_required
def dashboard(request):
    user = request.user

    print(user.user_type)

    universities = University.objects.all()
    commission_tiers = {}
    for university in universities:
        try:
            commission_tier = CommissionTier.objects.get(user=user, university=university)
            commission_tiers[university.pk] = commission_tier
        except CommissionTier.DoesNotExist:
            commission_tiers[university.pk] = None

    if user.is_admin:
        pending_agents = CustomUser.objects.filter(is_active=False)
        total_agent = CustomUser.objects.all().count()
        context = {
            'user_type': UserType.ADMIN,
            'pending_agents': pending_agents,
            'total_agent': total_agent
        }
    elif user.is_agent:
        context = {
            'user_type': UserType.AGENT,
            'commission_tiers': commission_tiers,
            'universities': universities,
            'agent': user
        }
    elif user.is_sub_agent:
        context = {
            'user_type': UserType.SUB_AGENT,
            'commission_tiers': commission_tiers,
            'universities': universities,
            'agent': user
        }
    elif user.is_exclusive_agent:
        context = {
            'user_type': UserType.EXCLUSIVE_AGENT,
            'commission_tiers': commission_tiers,
            'universities': universities,
            'agent': user
        }
    return render(request, 'portal/dashboard.html', context)

@login_required
@admin_required
def all_agent(request):
    user = request.user
    if user.is_admin:
        agents = CustomUser.objects.all().order_by('-date_joined')
        context = {
            'agents': agents
        }
        return render(request, 'portal/all_agents.html', context)
    else:
        return redirect('core:dashboard')

@login_required
@any_user_required
def my_agents(request):
    user = request.user
    if not user.is_admin:
        agents = CustomUser.objects.filter(referred_by=request.user).order_by('-date_joined')
        print(agents)
        context = {
            'agents': agents
        }
        return render(request, 'portal/my_agents.html', context)
    else:
        return redirect('core:dashboard')


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
    referrals = CustomUser.objects.filter(referred_by=user.id)
    documents = DocumentImage.objects.filter(identification_document__user=user)
    try:
        company = Company.objects.get(user=user)
        trade_license = company.trade_license
    except Company.DoesNotExist:
        trade_license = None
    if request.method == 'POST':
        post_code = request.POST.get('post_code')
        is_verified = request.POST.get('is_verified')
        is_active = request.POST.get('is_active')
        user_type = request.POST.get('user_type')

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
            user.user_type = user_type
            user.save()
            messages.success(request, 'Profile updated successfully.')
    return render(request, 'portal/profile_manage.html', {'user':user, 'documents': documents, 'trade_license': trade_license, 'referrals':referrals})

@login_required
@admin_exclusive_required
def comission_manage(request, pk):
    user = CustomUser.objects.get(id=pk)
    if request.method == 'POST':
        universities = University.objects.all()
        for university in universities:
            foundation = request.POST.get(f'foundation_{university.pk}')
            diploma = request.POST.get(f'diploma_{university.pk}')
            bachelor = request.POST.get(f'bachelor_{university.pk}')
            masters = request.POST.get(f'masters_{university.pk}')
            phd = request.POST.get(f'phd_{university.pk}')
            research = request.POST.get(f'research_{university.pk}')

            try:
                foundation = request.POST.get(f'foundation_{university.pk}', '0.0')
                diploma = request.POST.get(f'diploma_{university.pk}', '0.0')
                bachelor = request.POST.get(f'bachelor_{university.pk}', '0.0')
                masters = request.POST.get(f'masters_{university.pk}', '0.0')
                phd = request.POST.get(f'phd_{university.pk}', '0.0')
                research = request.POST.get(f'research_{university.pk}', '0.0')

                if foundation:
                    foundation = Decimal(foundation)
                else:
                    foundation = Decimal('0.0')

                if diploma:
                    diploma = Decimal(diploma)
                else:
                    diploma = Decimal('0.0')

                if bachelor:
                    bachelor = Decimal(bachelor)
                else:
                    bachelor = Decimal('0.0')

                if masters:
                    masters = Decimal(masters)
                else:
                    masters = Decimal('0.0')

                if phd:
                    phd = Decimal(phd)
                else:
                    phd = Decimal('0.0')

                if research:
                    research = Decimal(research)
                else:
                    research = Decimal('0.0')

                DecimalValidator(max_digits=10, decimal_places=2)(foundation)
                DecimalValidator(max_digits=10, decimal_places=2)(diploma)
                DecimalValidator(max_digits=10, decimal_places=2)(bachelor)
                DecimalValidator(max_digits=10, decimal_places=2)(masters)
                DecimalValidator(max_digits=10, decimal_places=2)(phd)
                DecimalValidator(max_digits=10, decimal_places=2)(research)

                commission_tier, created = CommissionTier.objects.get_or_create(user=user, university=university)
                if request.user.user_type == 'Admin':
                    commission_tier.status = True
                else:
                    commission_tier.status = False
                commission_tier.foundation_commission = foundation
                commission_tier.diploma_commission = diploma
                commission_tier.bachelor_commission = bachelor
                commission_tier.masters_commission = masters
                commission_tier.phd_commission = phd
                commission_tier.research_based_commission = research
                commission_tier.save()

            except (ValueError, DjangoValidationError) as e:
                messages.error(request, f"Validation error for university {university.name}: {str(e)}")


        messages.success(request, "Commission tiers updated successfully.")
        return redirect('core:comission_manage', user.id)

    universities = University.objects.all()
    commission_tiers = {}
    for university in universities:
        try:
            commission_tier = CommissionTier.objects.get(user=user, university=university)
            commission_tiers[university.pk] = commission_tier
        except CommissionTier.DoesNotExist:
            commission_tiers[university.pk] = None

    # print(commission_tiers[1].foundation_commission)
            
    context = {
        'universities': universities,
        'commission_tiers': commission_tiers,
        'agent': user
    }
    return render(request, 'portal/comission_manage.html', context)


@login_required
@any_user_required
def university(request):
    user = request.user
    if user.is_admin:
        if request.method == "POST":
            name = request.POST.get('name')
            if name:
                try:
                    University.objects.create(name=name)
                    messages.success(request, f"University '{name}' created successfully.")
                except Exception as e:
                    messages.error(request, f"Failed to create university: {e}")
                return redirect('core:university')
            else:
                messages.error(request, "Name field must be required")

        universitys = University.objects.all().order_by('-id')
        context = {
            'user_type': UserType.ADMIN,
            'universitys': universitys
        }
    elif user.is_agent:
        universitys = University.objects.all().order_by('-id')
        context = {
            'user_type': UserType.AGENT,
            'universitys': universitys
        }
    elif user.is_sub_agent:
        universitys = University.objects.all().order_by('-id')
        context = {
            'user_type': UserType.SUB_AGENT,
            'universitys': universitys
        }
    elif user.is_exclusive_agent:
        universitys = University.objects.all().order_by('-id')
        context = {
            'user_type': UserType.EXCLUSIVE_AGENT,
            'universitys': universitys
        }
    return render(request, 'portal/university.html', context)

@login_required
@admin_required
def university_edit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        un_id = request.POST.get('un_id')
        if name and un_id:
            try:
                university = University.objects.get(pk=un_id)
                university.name = name
                university.save()
                messages.success(request, f"University '{name}' updated successfully.")
            except University.DoesNotExist:
                messages.error(request, "University not found.")
            except Exception as e:
                messages.error(request, f"Failed to update university: {e}")
        else:
            messages.error(request, "Name field must be provided")

    return redirect('core:university')

@login_required
@admin_required
def university_delete(request, pk):
    university = University.objects.get(pk=pk)
    name = university.name
    if university.delete():
        messages.success(request, f"University '{name}' deleted successfully.")
    return redirect('core:university')

@login_required
def application(request):
    universitys = University.objects.all()
    applications = Applicant.objects.filter(user=request.user).order_by('-id')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        passport_number = request.POST.get('passport_number')
        dob = request.POST.get('dob')
        university_id = request.POST.get('university')
        subject = request.POST.get('subject')
        program = request.POST.get('program')

        if not (first_name and last_name and passport_number and dob and university_id and subject and program):
            messages.error(request, "Please fill in all required fields.")
            return redirect('core:application')
            
        application_id = generate_unique_id()

        try:
            university_obj = University.objects.get(pk=university_id)
        except University.DoesNotExist:
            messages.error(request, "Invalid university selected.")
            return redirect('core:application')

        applicant = Applicant.objects.create(
            first_name=first_name,
            last_name=last_name,
            passport_number=passport_number,
            dob=dob,
            university=university_obj,
            subject=subject,
            program=program,
            application_id=application_id,
            user=request.user
        )
        messages.success(request, "Application submitted successfully!")

    return render(request, 'portal/application.html', {'universitys':universitys, 'applicaitons': applications})

def generate_unique_id():
    length = 8
    characters = string.ascii_uppercase + string.digits
    invoice_id = ''.join(random.choice(characters) for _ in range(length))
    return invoice_id

@login_required
def application_status(request, pk):
    application = Applicant.objects.get(id=pk)
    statuses = ApplicationStatus.objects.filter(application=application).order_by('-id')
    latest_status = ApplicationStatus.objects.filter(application=application).order_by('-id')[:1]
    return render(request, 'portal/application_status.html', {'statuses':statuses, 'application':application, 'latest_status':latest_status})

@login_required
@admin_required
def admin_application(request):
    applications = Applicant.objects.all().order_by('-id')
    context = {
        'applications':applications
    }
    return render(request, 'portal/admin_application.html', context)


@login_required
@admin_required
def admin_manage_status(request, pk):
    application = Applicant.objects.get(id=pk)
    statuses = ApplicationStatus.objects.filter(application=application).order_by('-id')
    context = {
        'application':application,
        'statuses': statuses
    }
    if request.method == "POST":
        status = request.POST.get('status')
        remark = request.POST.get('remark')
        if not (status and remark):
            messages.error(request, "Please fill in all required fields.")
            return redirect('core:admin_manage_status', application.id)
        application_status = ApplicationStatus.objects.create(
            status=status,
            remark=remark,
            application=application
        )
        messages.success(request, "Status Added successfully!")
    return render(request, 'portal/admin_manage_status.html', context)
