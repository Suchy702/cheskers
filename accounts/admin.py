from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Info


class InfoInline(admin.StackedInline):
    model = Info
    can_delete = False
    verbose_name_plural = 'infos'


class UserAdmin(BaseUserAdmin):
    inlines = (InfoInline,)


# Re-register UserAdmin
admin.site.register(Info)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
