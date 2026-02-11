from django.contrib import admin
from .models import DailyReport,DailyReportAttachment
# Register your models here.

admin.site.register(DailyReport)
admin.site.register(DailyReportAttachment)