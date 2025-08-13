from django.contrib import admin
from .models import Lead
# Register your models here.
admin.site.register(Lead)

class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'program', 'priority', 'source')
    list_filter = ('status', 'program', 'priority', 'source')
    search_fields = ('name', 'phone', 'email')