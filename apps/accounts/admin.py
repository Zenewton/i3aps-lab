from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "institution", "user_type", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name", "institution")
    list_filter = ("user_type", "created_at")
