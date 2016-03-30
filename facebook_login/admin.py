from django.contrib import admin

from facebook_login.models import FacebookProfile


class FacebookProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'facebook_id', 'access_token', 'profile_data')
    list_filter = ('user__first_name', 'user__last_name', 'user__email', 'facebook_id')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'facebook_id')


admin.site.register(FacebookProfile, FacebookProfileAdmin)
