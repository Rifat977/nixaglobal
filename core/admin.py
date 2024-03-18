from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(University)
admin.site.register(CommissionTier)
admin.site.register(Applicant)
admin.site.register(ApplicationStatus)
admin.site.register(PaymentRequest)

admin.site.register(Subject)



class FeeAdmin(admin.ModelAdmin):
    list_display = ('subject', 'field_name', 'value')
    list_filter = ('subject', 'field_name')
    search_fields = ('subject__name', 'subject__university__name', 'subject__program_type', 'field_name', 'value')

admin.site.register(Fee, FeeAdmin)
