from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group)
admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(IdentificationDocument)
admin.site.register(DocumentImage)
admin.site.register(Referral)
admin.site.register(Notification)