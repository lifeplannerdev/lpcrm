from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.landing_page, name='landing'),  # Handles GET requests
    path('quick-login/', views.quick_login, name='quick_login'),  # Handles POST
    path('dashboard/', views.admission_dashboard, name='admission_dashboard'),
    path('executive-dashboard/', views.admission_executive_dashboard, name='admission_executive_dashboard'),
    path('media/', views.media_dashboard, name='media_dashboard'),
    path('operations/', views.operations_dashboard, name='operations_dashboard'),
    path('assign-lead/', views.assign_lead, name='assign_lead'),
    path('forward-to-processing/', views.forward_to_processing, name='forward_to_processing'),
    path('update-lead-field/', views.update_lead_field, name='update_lead_field'),
    path('processing/', views.ProcessingDashboard.as_view(), name='processing_dashboard'),
    path('accept-lead/', views.accept_lead, name='accept_lead'),
    path('complete-processing/', views.complete_processing, name='complete_processing'),
    path('hold-processing/', views.hold_processing, name='hold_processing'),
    path('reject-lead/', views.reject_lead, name='reject_lead'),
    path('update-document-status/', views.update_document_status, name='update_document_status'),
    path('update-processing-notes/', views.update_processing_notes, name='update_processing_notes'),
    path('reopen-lead/', views.reopen_lead, name='reopen_lead'),
    path('all-leads/', views.all_leads, name='all_leads'),
    path('import_leads_excel/', views.import_leads_excel, name='import_leads_excel'),
    path('download_excel_template/', views.download_excel_template, name='download_excel_template'),
    path('delete-lead/<int:lead_id>/', views.delete_lead, name='delete_lead'),
    path('leads/assign-to-executive/', views.assign_lead_to_executive, name='assign_to_executive'),
    path('add-lead/', views.add_lead, name='add_lead'),
    path('lead-details/<int:lead_id>/', views.lead_details, name='lead_details'),
    path('daily-report/', views.submit_daily_report, name='daily_report'),
    path('report-history/', views.daily_report_history, name='report_history'),
    
]