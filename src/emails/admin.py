from django.contrib import admin
from .models import (
    Email, 
    EmailVerification
)

# Register your models here.

@admin.register(Email)
class EmailAdminModels(admin.ModelAdmin):
    list_display = ['email', 'timestamp']
    fields = ['email', 'timestamp', 'activate']
    readonly_fields = ['timestamp', 'email']
    list_filter = ['timestamp']


@admin.register(EmailVerification) 
class EmailVarification(admin.ModelAdmin):
    list_display = ['email', 'attempts', 'expired_at']
    list_filter = ['expired', 'expired_at', 'attempts']
    fields = ['parent', 'email', 'expired', 'expired_at', 'timestamp']
    readonly_fields = ['expired', 'email', 'timestamp', 'expired_at', 'parent', 'attempts']