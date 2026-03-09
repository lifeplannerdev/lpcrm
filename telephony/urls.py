from django.urls import path
from .views import voxbay_webhook, call_logs_list

urlpatterns = [
    path("voxbay/webhook/",    voxbay_webhook), 
    path("voxbay/call-logs/",  call_logs_list),  
]