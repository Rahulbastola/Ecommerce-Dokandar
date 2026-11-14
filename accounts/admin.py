
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Details', {
            'fields': (
                'full_name',
                'phone',
                'address',
                'profile_picture',
                'role',
            )
        }),
    )

    list_display = (
        'username',
        'email',
        'role',
        'phone',
        'is_staff',
    )
