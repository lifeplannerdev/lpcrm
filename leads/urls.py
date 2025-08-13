from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('<int:lead_id>/update_priority/', views.update_priority, name='update_priority'),
    path('<int:lead_id>/update_status/', views.update_status, name='update_status'),
    path('<int:lead_id>/update_program/', views.update_program, name='update_program'),
    
    
      
    
]