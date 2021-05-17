from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.functional import lazy
from django.utils.translation import gettext, gettext_lazy as _

from .models import CustomUser

gettext_lazy = lazy(gettext, str)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'balance')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
