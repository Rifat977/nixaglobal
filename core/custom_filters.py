# Create a file named 'custom_filters.py' in your Django app directory
from django import template
from .models import CommissionTier, Applicant
import re

register = template.Library()

@register.filter
def get_commission_tier_for_admin(university, user):
    try:
        return CommissionTier.objects.get(university=university, user=user)
    except CommissionTier.DoesNotExist:
        return None

@register.filter
def get_commission_tier(university, user):
    try:
        return CommissionTier.objects.get(university=university, user=user, status=True)
    except CommissionTier.DoesNotExist:
        return None

# @register.filter
# def get_total_fee_value(fees):
#     total_fee_value = 0
#     for fee in fees:
#         if fee.field_name == "Total":
#             value_without_commas = fee.value.replace(',', '')
#             match = re.search(r'\d+', value_without_commas)
#             if match:
#                 total_fee_value = match.group()
#             break
#     return int(total_fee_value)

@register.filter
def get_total_fee_value(fees):
    total_fee_value = 0
    for fee in fees:
        if fee.field_name == "Total":
            total_fee_value = fee.value
            break
    return f"{total_fee_value}"


@register.filter(name='get_agreed_commission')
def get_agreed_commission(applicant, user):
    agreed_commission = CommissionTier.objects.filter(user=user, university=applicant.subject.university).first()
    return agreed_commission

@register.filter(name='count_applications')
def count_applications(user):
    count_application = Applicant.objects.filter(user=user).count()
    return count_application