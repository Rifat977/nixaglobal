from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(University)


class CommissionTierAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # Disables adding new instances

class ApplicantAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # Disables adding new instances

class ApplicationStatusAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # Disables adding new instances

class PaymentRequestAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # Disables adding new instances

# Register the models with the customized admin classes
admin.site.register(CommissionTier, CommissionTierAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)

admin.site.register(Subject)


class FeeAdmin(admin.ModelAdmin):
    list_display = ('subject', 'field_name', 'value')
    list_filter = ('subject', 'field_name')
    search_fields = ('subject__name', 'subject__university__name', 'subject__program_type', 'field_name', 'value')

admin.site.register(Fee, FeeAdmin)
