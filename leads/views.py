from rest_framework import generics, filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import models
from django.utils import timezone
from leads.permissions import (
    CanAccessLeads, 
    CanAssignLeads,
    LEAD_VIEW_ALL_ROLES,
    ADMIN_ROLES,
    MANAGER_ROLES,
    EXECUTIVE_ROLES
)
from .models import Lead, ProcessingUpdate, RemarkHistory, LeadAssignment
from .serializers import (
    LeadListSerializer,
    LeadDetailSerializer,
    LeadCreateSerializer,
    ProcessingUpdateSerializer,
    LeadAssignSerializer,
    LeadAssignmentSerializer,
)

# Pagination 
class LeadPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


# Lead List View - UPDATED: Only ADMIN sees all leads
class LeadListView(generics.ListAPIView):
    serializer_class = LeadListSerializer
    permission_classes = [CanAccessLeads]  
    pagination_class = LeadPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['priority', 'status', 'source', 'processing_status', 'assigned_to', 'sub_assigned_to']
    search_fields = ['name', 'phone', 'email', 'program']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        
        # ONLY ADMIN can see all leads
        if user.role in ADMIN_ROLES:
            return Lead.objects.all().distinct()
        
        # All other roles (Managers, Executives, HR, etc.) see only their assigned leads
        return Lead.objects.filter(
            models.Q(assigned_to=user) | 
            models.Q(sub_assigned_to=user)
        ).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        # Stats for the user
        stats = {
            "new": queryset.filter(status__iexact='ENQUIRY').count(),
            "qualified": queryset.filter(status__iexact='QUALIFIED').count(),
            "converted": queryset.filter(status__iexact='CONVERTED').count(),
            "total_assigned": queryset.filter(assigned_to=request.user).count(),
            "total_sub_assigned": queryset.filter(sub_assigned_to=request.user).count(),
        }

        return self.get_paginated_response({
            "leads": serializer.data,
            "stats": stats,
        })


# Lead Create View 
class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadCreateSerializer
    permission_classes = [CanAccessLeads] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()

        # Track initial processing status if it's not PENDING
        if getattr(lead, 'processing_status', None) and lead.processing_status != 'PENDING':
            ProcessingUpdate.objects.create(
                lead=lead,
                status=lead.processing_status,
                changed_by=request.user,
                notes="Initial status on lead creation"
            )

        return Response({
            "message": "Lead created successfully",
            "lead_id": lead.id
        }, status=status.HTTP_201_CREATED)


# Lead Detail View - UPDATED: Only ADMIN sees all leads
class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeadDetailSerializer
    permission_classes = [CanAccessLeads]

    def get_queryset(self):
        user = self.request.user
        
        # ONLY ADMIN can access all leads
        if user.role in ADMIN_ROLES:
            return Lead.objects.all()
        
        # All other roles can only access their assigned leads
        return Lead.objects.filter(
            models.Q(assigned_to=user) | 
            models.Q(sub_assigned_to=user)
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        lead = self.get_object()
        old_processing_status = lead.processing_status

        serializer = self.get_serializer(
            lead,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)
        updated_lead = serializer.save()

        # Track processing_status change
        if old_processing_status != updated_lead.processing_status:
            ProcessingUpdate.objects.create(
                lead=updated_lead,
                status=updated_lead.processing_status,
                changed_by=request.user,
                notes="Status updated via API"
            )

        return Response(
            {
                "message": "Lead updated successfully",
                "lead": LeadDetailSerializer(updated_lead).data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(
            {"message": "Lead deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# Lead Processing Timeline View - UPDATED
class LeadProcessingTimelineView(generics.ListAPIView):
    serializer_class = ProcessingUpdateSerializer
    permission_classes = [CanAccessLeads]

    def get_queryset(self):
        lead_id = self.kwargs.get('lead_id')
        lead = get_object_or_404(Lead, id=lead_id)
        user = self.request.user
        
        # ONLY ADMIN or assigned users can view timeline
        if user.role in ADMIN_ROLES:
            return ProcessingUpdate.objects.filter(lead=lead).order_by('-timestamp')
        
        # Check if user is assigned to this lead
        if lead.assigned_to != user and lead.sub_assigned_to != user:
            return ProcessingUpdate.objects.none()
        
        return ProcessingUpdate.objects.filter(lead=lead).order_by('-timestamp')


# Lead Assignment View
class LeadAssignView(APIView):
    """
    Assign or sub-assign a lead
    POST /api/leads/assign/
    """
    permission_classes = [CanAssignLeads]

    def post(self, request):
        serializer = LeadAssignSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        lead = serializer.validated_data['lead']
        assignee = serializer.validated_data['assignee']
        assignment_type = serializer.validated_data['assignment_type']
        notes = serializer.validated_data.get('notes', '')
        
        if assignment_type == 'PRIMARY':
            # Admin assigning to manager/executive
            lead.assigned_to = assignee
            lead.assigned_by = request.user
            lead.assigned_date = timezone.now()
            # Clear sub-assignment if exists
            lead.sub_assigned_to = None
            lead.sub_assigned_by = None
            lead.sub_assigned_date = None
            
        elif assignment_type == 'SUB':
            # Manager sub-assigning to executive
            lead.sub_assigned_to = assignee
            lead.sub_assigned_by = request.user
            lead.sub_assigned_date = timezone.now()
        
        lead.save()
        
        # Create assignment history
        LeadAssignment.objects.create(
            lead=lead,
            assigned_to=assignee,
            assigned_by=request.user,
            assignment_type=assignment_type,
            notes=notes
        )
        
        return Response({
            'message': 'Lead assigned successfully',
            'lead': LeadDetailSerializer(lead).data
        }, status=status.HTTP_200_OK)


# Bulk Lead Assignment View
class BulkLeadAssignView(APIView):
    """
    Assign multiple leads at once
    POST /api/leads/bulk-assign/
    Body: {
        "lead_ids": [1, 2, 3],
        "assigned_to_id": 5,
        "notes": "Bulk assignment"
    }
    """
    permission_classes = [CanAssignLeads]

    def post(self, request):
        lead_ids = request.data.get('lead_ids', [])
        assigned_to_id = request.data.get('assigned_to_id')
        notes = request.data.get('notes', '')

        if not lead_ids or not isinstance(lead_ids, list):
            return Response(
                {'error': 'lead_ids must be a non-empty list'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not assigned_to_id:
            return Response(
                {'error': 'assigned_to_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        success_count = 0
        failed_leads = []

        for lead_id in lead_ids:
            try:
                # Use the same validation logic as LeadAssignSerializer
                serializer = LeadAssignSerializer(
                    data={'lead_id': lead_id, 'assigned_to_id': assigned_to_id, 'notes': notes},
                    context={'request': request}
                )
                
                if serializer.is_valid():
                    lead = serializer.validated_data['lead']
                    assignee = serializer.validated_data['assignee']
                    assignment_type = serializer.validated_data['assignment_type']
                    
                    if assignment_type == 'PRIMARY':
                        lead.assigned_to = assignee
                        lead.assigned_by = user
                        lead.assigned_date = timezone.now()
                        lead.sub_assigned_to = None
                        lead.sub_assigned_by = None
                        lead.sub_assigned_date = None
                    elif assignment_type == 'SUB':
                        lead.sub_assigned_to = assignee
                        lead.sub_assigned_by = user
                        lead.sub_assigned_date = timezone.now()
                    
                    lead.save()
                    
                    LeadAssignment.objects.create(
                        lead=lead,
                        assigned_to=assignee,
                        assigned_by=user,
                        assignment_type=assignment_type,
                        notes=notes
                    )
                    success_count += 1
                else:
                    failed_leads.append({'lead_id': lead_id, 'errors': serializer.errors})
            except Exception as e:
                failed_leads.append({'lead_id': lead_id, 'error': str(e)})

        return Response({
            'message': f'Successfully assigned {success_count} leads',
            'success_count': success_count,
            'failed_count': len(failed_leads),
            'failed_leads': failed_leads
        }, status=status.HTTP_200_OK)


# Lead Assignment History View - UPDATED
class LeadAssignmentHistoryView(generics.ListAPIView):
    """
    Get assignment history for a specific lead
    GET /api/leads/{lead_id}/assignment-history/
    """
    serializer_class = LeadAssignmentSerializer
    permission_classes = [CanAccessLeads]

    def get_queryset(self):
        lead_id = self.kwargs.get('lead_id')
        lead = get_object_or_404(Lead, id=lead_id)
        user = self.request.user
        
        # ONLY ADMIN or assigned users can view history
        if user.role in ADMIN_ROLES:
            return LeadAssignment.objects.filter(lead=lead).order_by('-timestamp')
        
        # Check if user is assigned to this lead
        if lead.assigned_to != user and lead.sub_assigned_to != user:
            return LeadAssignment.objects.none()
        
        return LeadAssignment.objects.filter(lead=lead).order_by('-timestamp')


# My Team Leads View - UPDATED
class MyTeamLeadsView(generics.ListAPIView):
    """
    Get all leads for manager's team
    GET /api/leads/my-team/
    
    NOTE: This endpoint is now only useful for ADMIN roles.
    Managers will only see their directly assigned leads in the main list.
    """
    serializer_class = LeadListSerializer
    permission_classes = [CanAccessLeads]
    pagination_class = LeadPagination

    def get_queryset(self):
        user = self.request.user
        
        # Only ADMIN can see team leads
        if user.role in ADMIN_ROLES:
            # Return all leads (same as main list for admin)
            return Lead.objects.all().distinct()
        
        # For managers and others, return only their assigned leads
        return Lead.objects.filter(
            models.Q(assigned_to=user) |
            models.Q(sub_assigned_to=user)
        ).distinct()


# Available Users for Assignment
class AvailableUsersForAssignmentView(APIView):
    """
    Get list of users that can be assigned leads
    GET /api/leads/available-users/
    """
    permission_classes = [CanAssignLeads]

    def get(self, request):
        from accounts.models import User
        user = request.user
        
        if user.role in ADMIN_ROLES:
            # Admin can assign to managers and executives
            users = User.objects.filter(
                role__in=MANAGER_ROLES + EXECUTIVE_ROLES,
                is_active=True
            ).values('id', 'username', 'email', 'role', 'first_name', 'last_name')
            
        elif user.role in MANAGER_ROLES:
            # Manager can sub-assign to executives only
            users = User.objects.filter(
                role__in=EXECUTIVE_ROLES,
                is_active=True
            ).values('id', 'username', 'email', 'role', 'first_name', 'last_name')
        else:
            return Response(
                {'error': 'You do not have permission to assign leads'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(list(users), status=status.HTTP_200_OK)


# Unassign Lead
class UnassignLeadView(APIView):
    """
    Remove assignment from a lead
    POST /api/leads/unassign/
    Body: {
        "lead_id": 1,
        "unassign_type": "PRIMARY" or "SUB"
    }
    """
    permission_classes = [CanAssignLeads]

    def post(self, request):
        lead_id = request.data.get('lead_id')
        unassign_type = request.data.get('unassign_type', 'SUB')  # Default to SUB
        
        if not lead_id:
            return Response(
                {'error': 'lead_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return Response(
                {'error': 'Lead not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user = request.user
        
        # Check permissions
        if user.role in ADMIN_ROLES:
            # Admin can unassign both primary and sub
            if unassign_type == 'PRIMARY':
                lead.assigned_to = None
                lead.assigned_by = None
                lead.assigned_date = None
                lead.sub_assigned_to = None
                lead.sub_assigned_by = None
                lead.sub_assigned_date = None
            elif unassign_type == 'SUB':
                lead.sub_assigned_to = None
                lead.sub_assigned_by = None
                lead.sub_assigned_date = None
                
        elif user.role in MANAGER_ROLES:
            # Manager can only unassign sub-assignments for their leads
            if lead.assigned_to != user:
                return Response(
                    {'error': 'You can only unassign leads assigned to you'},
                    status=status.HTTP_403_FORBIDDEN
                )
            lead.sub_assigned_to = None
            lead.sub_assigned_by = None
            lead.sub_assigned_date = None
        else:
            return Response(
                {'error': 'You do not have permission to unassign leads'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        lead.save()
        
        return Response({
            'message': 'Lead unassigned successfully',
            'lead': LeadDetailSerializer(lead).data
        }, status=status.HTTP_200_OK)
