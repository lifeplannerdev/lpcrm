# notifications/urls.py
from django.urls import path
from .views import NotificationListView, MarkNotificationsReadView, ClearNotificationsView

urlpatterns = [
    path('notifications/', NotificationListView.as_view()),
    path('notifications/mark-read/', MarkNotificationsReadView.as_view()),
    path('notifications/clear/', ClearNotificationsView.as_view()),
]