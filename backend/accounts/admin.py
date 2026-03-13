from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetOTP


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("id", "email", "phone_number", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    ordering = ("email",)
    search_fields = ("email", "phone_number")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("phone_number", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(PasswordResetOTP)