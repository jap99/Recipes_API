from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

# the recommended convention for converting string to human readable text
    # we do it so it gets passed through the translation engine; in case u wanted to extend the code to support multiple languages
        # you'd just setup the translation files and it'll convert the text accordingly
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id'] # set the ordering to the id of the object
    list_display = ['email', 'name'] # list them by email and name
    # define the sections for the field set in our change and create page
        # each bracked in paranthesis is a section
        # title of first section is NONE - has the email & pw fields
        # second section - personal info - first import the getText function
        # third - the controls that control the user
    fieldsets = (
        (None, {'fields': ('email', 'password') }),
        (_('Personal Info'), {'fields': ('name',)}), # if just one field (as is this case) add a comma at the end so it's not read as a string
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    # customized to include our email & pw
    add_fieldsets = (
        (None, {
            'classes': ('wide',), # the classes taht are assigned to the form. default is that it has a wide class
            'fields': ('email', 'password1', 'password2')
        }),
    )

    # register in the django admin
admin.site.register(models.User, UserAdmin) # register our UserAdmin to the model that's passed in
admin.site.register(models.Tag) # don't need to specify the admin we want to register it with; uses the default one for the model
admin.site.register(models.Ingredient) 
admin.site.register(models.Recipe)