from django.contrib import admin
from .models import Trainer, Student

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'drive_link')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('status',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch', 'trainer', 'status', 'admission_date')
    list_filter = ('batch', 'status', 'trainer')
    search_fields = ('name',)
    raw_id_fields = ('trainer',)