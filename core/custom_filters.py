# Create a file named 'custom_filters.py' in your Django app directory
from django import template
from .models import CommissionTier

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
