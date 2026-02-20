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
    UpdateLeadView,
)

urlpatterns = [
    # Static paths MUST come before dynamic <int:pk> paths
    # otherwise Django matches them as pk and never reaches these views
    path('leads/', LeadListView.as_view(), name='lead-list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/assign/', LeadAssignView.as_view(), name='lead-assign'),
    path('leads/bulk-assign/', BulkLeadAssignView.as_view(), name='bulk-lead-assign'),
    path('leads/unassign/', UnassignLeadView.as_view(), name='lead-unassign'),
    path('leads/my-team/', MyTeamLeadsView.as_view(), name='my-team-leads'),
    path('leads/available-users/', AvailableUsersForAssignmentView.as_view(), name='available-users'),

    # Dynamic paths after static paths
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('leads/<int:pk>/update/', UpdateLeadView.as_view(), name='lead-update'),
    path('leads/<int:lead_id>/timeline/', LeadProcessingTimelineView.as_view(), name='lead-timeline'),
    path('leads/<int:lead_id>/assignment-history/', LeadAssignmentHistoryView.as_view(), name='lead-assignment-history'),
]