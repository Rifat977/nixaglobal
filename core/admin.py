from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(University)
admin.site.register(CommissionTier)
admin.site.register(Applicant)
admin.site.register(ApplicationStatus)
admin.site.register(PaymentRequest)