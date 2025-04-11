from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'is_banned')
    list_editable = ('is_banned',)

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    user_username.short_description = 'Username'
    user_email.short_description = 'Email'

admin.site.register(Profile, ProfileAdmin)
# Register your models here.
