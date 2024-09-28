from django.contrib import admin

from accounts.models import UserAction, Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    """
        A custom ModelAdmin for the Profile model in Django admin interface.

        Allows detailed configuration of Profile entry forms and defines displayed columns in listing.

        Attributes
        ----------
        fields : tuple
            Specifies the fields to display when adding or changing a Profile instance in the admin interface.
        list_display : tuple
            Specifies the fields to display in the list view of Profile instances in the admin interface.
    """

    fields = ('user', 'image')
    list_display = ('user', 'image')


class UserActionAdmin(admin.ModelAdmin):
    """
        Admin interface definition for the UserAction model.

        Fields:
            fields (tuple): Specifies the fields to be displayed in the model form.
            readonly_fields (tuple): Specifies the fields that are read-only.
            list_display (tuple): Specifies the fields to be displayed in the model list view.
    """

    fields = ('user', 'action')
    readonly_fields = ('write_date', )
    list_display = ('user', 'write_date', 'action')


admin.site.register(Profile, ProfileAdmin)

admin.site.register(UserAction, UserActionAdmin)
