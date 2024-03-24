from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group)
admin.site.register(CustomUser)




class NotAddableModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

admin.site.register(Company, NotAddableModelAdmin)
admin.site.register(IdentificationDocument, NotAddableModelAdmin)
admin.site.register(DocumentImage, NotAddableModelAdmin)


class NotificationAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False 
    
    def has_add_permission(self, request):
        return False 

admin.site.register(Notification, NotificationAdmin)