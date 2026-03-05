from django.urls import path
from .views import voxbay_webhook

urlpatterns = [
    path("api/voxbay/webhook/", voxbay_webhook),
]