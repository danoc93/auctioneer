from user_auth.models.User import User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)