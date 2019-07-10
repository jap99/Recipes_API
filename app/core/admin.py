from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models




class UserAdmin(BaseUserAdmin):
    ordering = ['id'] # set the ordering to the id of the object
    list_display = ['email', 'name'] # list them by email and name

    # register in the django admin
admin.site.register(models.User, UserAdmin) # register our UserAdmin to the model that's passed in
