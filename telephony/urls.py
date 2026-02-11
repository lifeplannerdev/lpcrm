from django.urls import path
from .views import VoxbayWebhookAPIView

urlpatterns = [
    path("voxbay/webhook/", VoxbayWebhookAPIView.as_view(), name="voxbay-webhook"),
]
