from django.urls import path
from .views import (
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadProcessingTimelineView,
    LeadAssignView,
    BulkLeadAssignView,
    LeadAssignmentHistoryView,
    MyTeamLeadsView,
    AvailableUsersForAssignmentView,
    UnassignLeadView,
)

urlpatterns = [
    # Existing endpoints
    path('leads/', LeadListView.as_view(), name='lead-list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('leads/<int:lead_id>/timeline/', LeadProcessingTimelineView.as_view(), name='lead-timeline'),
    
    path('leads/assign/', LeadAssignView.as_view(), name='lead-assign'),
    path('leads/bulk-assign/', BulkLeadAssignView.as_view(), name='bulk-lead-assign'),
    path('leads/unassign/', UnassignLeadView.as_view(), name='lead-unassign'),
    path('leads/<int:lead_id>/assignment-history/', LeadAssignmentHistoryView.as_view(), name='lead-assignment-history'),
    path('leads/my-team/', MyTeamLeadsView.as_view(), name='my-team-leads'),
    path('leads/available-users/', AvailableUsersForAssignmentView.as_view(), name='available-users'),
]