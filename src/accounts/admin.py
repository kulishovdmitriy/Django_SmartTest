from django.contrib import admin

from accounts.models import UserAction, Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'image')
    list_display = ('user', 'image')


class UserActionAdmin(admin.ModelAdmin):
    fields = ('user', 'action')
    readonly_fields = ('write_date', )
    list_display = ('user', 'write_date', 'action')


admin.site.register(Profile, ProfileAdmin)

admin.site.register(UserAction, UserActionAdmin)
