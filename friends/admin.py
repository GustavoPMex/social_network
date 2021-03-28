from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserFriends

# Register your models here.

admin.site.register(UserFriends, UserAdmin)

