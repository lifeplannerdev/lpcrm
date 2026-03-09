from django.urls import path
from .views import (
    VoxbayWebhookView,
    CallLogListView,
    CallStatsView,
    ClickToCallView,
)

urlpatterns = [
    path("voxbay/webhook/",       VoxbayWebhookView.as_view()),
    path("voxbay/call-logs/",     CallLogListView.as_view()),
    path("voxbay/stats/",         CallStatsView.as_view()),
    path("voxbay/click-to-call/", ClickToCallView.as_view()),
]