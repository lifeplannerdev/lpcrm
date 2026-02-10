from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.admin import AdminSite
from django.contrib.auth import BACKEND_SESSION_KEY
from django.conf import settings
from .models import MicroWork

class CustomUserAdmin(UserAdmin):
    # Makes password field more prominent
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email','location','phone ',)}),
        ('Role info', {'fields': ('role', 'team','salary')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(MicroWork)

# Unregister the Group model so it does not appear in admin
admin.site.unregister(Group)

# In your_app/admin.py or accounts/admin.py
admin.site.site_header = 'LP ADMINISTRATION'
admin.site.site_title = 'LP Admin Portal'
admin.site.index_title = 'Welcome to LP Administration'


