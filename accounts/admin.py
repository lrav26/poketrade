from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'poke_coins', 'is_banned')
    list_editable = ('poke_coins', 'is_banned')
    search_fields = ('user__username', 'user__email')
    list_filter = ('is_banned',)

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    user_username.short_description = 'Username'
    user_email.short_description = 'Email'

admin.site.register(Profile, ProfileAdmin)
