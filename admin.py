from django.contrib import admin
from .models import UserProfile, File


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'storage_used')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'size', 'uploaded_at', 'is_deleted')
    list_filter = ('is_deleted', 'uploaded_at')
    search_fields = ('name', 'owner__username')
