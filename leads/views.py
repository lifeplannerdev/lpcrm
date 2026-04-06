import pandas as pd
import math
from datetime import date
from .models import Lead, ProcessingUpdate, RemarkHistory, LeadAssignment
from .email_utils import send_conversion_email
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.db import models, transaction
from django.db.models import Count, Q as DQ
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser

from leads.permissions import (
    CanAccessLeads,
    CanAssignLeads,
    CanViewAllLeads,
    CanModifyAllLeads,
    FULL_ACCESS_ROLES,
    MANAGER_ROLES,
    EXECUTIVE_ROLES,
)

from .serializers import (
    LeadListSerializer,
    LeadDetailSerializer,
    LeadCreateSerializer,
    ProcessingUpdateSerializer,
    LeadAssignSerializer,
    LeadAssignmentSerializer,
    LeadUpdateSerializer,
    BulkLeadCreateSerializer,
)

from utils.pusher import pusher_client, trigger_pusher
from utils import notify_lead_assigned


# ── Helpers
def clean_value(val):
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return val


# ── Pagination
class LeadPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ── Lead List View
class LeadListView(generics.ListAPIView):
    serializer_class = LeadListSerializer
    permission_classes = [CanAccessLeads]
    pagination_class = LeadPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'priority':          ['exact'],
        'status':            ['exact', 'iexact'],
        'source':            ['exact'],
        'processing_status': ['exact'],
        'assigned_to':       ['exact', 'isnull'],
        'sub_assigned_to':   ['exact'],
    }
    search_fields   = ['name', 'phone', 'email', 'program']
    ordering_fields = ['created_at', 'priority']
    ordering        = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        base_qs = Lead.objects.select_related(
            'assigned_to', 'assigned_by',
            'sub_assigned_to', 'sub_assigned_by',
        )
        if user.role in FULL_ACCESS_ROLES:
            return base_qs.all().distinct()
        return base_qs.filter(
            models.Q(assigned_to=user) |
            models.Q(sub_assigned_to=user)
        ).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        stats = queryset.aggregate(
            new=Count('id', filter=DQ(status__iexact='ENQUIRY')),
            qualified=Count('id', filter=DQ(status__iexact='QUALIFIED')),
            converted=Count('id', filter=DQ(status__iexact='CONVERTED')),
            total_assigned=Count('id', filter=DQ(assigned_to=request.user)),
            total_sub_assigned=Count('id', filter=DQ(sub_assigned_to=request.user)),
        )

        return self.get_paginated_response({
            'leads': serializer.data,
            'stats': stats,
        })


# ── Lead Create View
class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadCreateSerializer
    permission_classes = [CanAccessLeads]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()

        if getattr(lead, 'processing_status', None) and lead.processing_status != 'PENDING':
            ProcessingUpdate.objects.create(
                lead=lead,
                status=lead.processing_status,
                changed_by=request.user,
                notes='Initial status on lead creation'
            )

        return Response({
            'message': 'Lead created successfully',
            'lead_id': lead.id
        }, status=status.HTTP_201_CREATED)


# ── Lead Detail / Update / Delete View
class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeadDetailSerializer
    permission_classes = [CanAccessLeads]

    def get_queryset(self):
        user = self.request.user
        base_qs = Lead.objects.select_related(
            'assigned_to', 'assigned_by',
            'sub_assigned_to', 'sub_assigned_by',
        )
        if user.role in FULL_ACCESS_ROLES:
            return base_qs.all()
        return base_qs.filter(
            models.Q(assigned_to=user) |
            models.Q(sub_assigned_to=user)
        )

    def update(self, request, *args, **kwargs):
        partial  = kwargs.pop('partial', False)
        lead     = self.get_object()
        old_processing_status = lead.processing_status
        old_status            = lead.status

        serializer = self.get_serializer(lead, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_lead = serializer.save()

        if old_processing_status != updated_lead.processing_status:
            ProcessingUpdate.objects.create(
                lead=updated_lead,
                status=updated_lead.processing_status,
                changed_by=request.user,
                notes='Status updated via API'
            )

        if old_status != 'CONVERTED' and updated_lead.status == 'CONVERTED':
            send_conversion_email(updated_lead)

        return Response({
            'message': 'Lead updated successfully',
            'lead': LeadDetailSerializer(updated_lead).data,
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if request.user.role not in FULL_ACCESS_ROLES:
            return Response(
                {'error': 'You do not have permission to delete leads'},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(self.get_object())
        return Response(
            {'message': 'Lead deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )


# ── Lead Processing Timeline View
class LeadProcessingTimelineView(generics.ListAPIView):
    serializer_class = ProcessingUpdateSerializer
    permission_classes = [CanAccessLeads]

    def get_queryset(self):
        lead_id = self.kwargs.get('lead_id')
        lead    = get_object_or_404(Lead, id=lead_id)
        user    = self.request.user

        if user.role in FULL_ACCESS_ROLES:
            return ProcessingUpdate.objects.filter(lead=lead).order_by('-timestamp')

        if lead.assigned_to != user and lead.sub_assigned_to != user:
            return ProcessingUpdate.objects.none()

        return ProcessingUpdate.objects.filter(lead=lead).order_by('-timestamp')


# ── Lead Assignment View
class LeadAssignView(APIView):
    permission_classes = [CanAssignLeads]

    def post(self, request):
        serializer = LeadAssignSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        lead            = serializer.validated_data['lead']
        assignee        = serializer.validated_data['assignee']
        assignment_type = serializer.validated_data['assignment_type']
        notes           = serializer.validated_data.get('notes', '')

        if assignment_type == 'PRIMARY':
            lead.assigned_to       = assignee
            lead.assigned_by       = request.user
            lead.assigned_date     = timezone.now()
            lead.sub_assigned_to   = None
            lead.sub_assigned_by   = None
            lead.sub_assigned_date = None

        elif assignment_type == 'SUB':
            lead.sub_assigned_to   = assignee
            lead.sub_assigned_by   = request.user
            lead.sub_assigned_date = timezone.now()

        lead.save()

        LeadAssignment.objects.create(
            lead=lead,
            assigned_to=assignee,
            assigned_by=request.user,
            assignment_type=assignment_type,
            notes=notes,
        )

        if assignee != request.user:
            notify_lead_assigned(
                assignee=assignee,
                assigned_by=request.user,
                lead=lead,
                assignment_type=assignment_type,
            )

        return Response({
            'message': 'Lead assigned successfully',
            'lead': LeadDetailSerializer(lead).data,
        }, status=status.HTTP_200_OK)


# ── Bulk Lead Assignment View
class BulkLeadAssignView(APIView):
    permission_classes = [CanAssignLeads]

    def post(self, request):
        lead_ids       = request.data.get('lead_ids', [])
        assigned_to_id = request.data.get('assigned_to_id')
        notes          = request.data.get('notes', '')

        if not lead_ids or not isinstance(lead_ids, list):
            return Response(
                {'error': 'lead_ids must be a non-empty list'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not assigned_to_id:
            return Response(
                {'error': 'assigned_to_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user          = request.user
        success_count = 0
        failed_leads  = []
        assigned_summary = {}

        for lead_id in lead_ids:
            try:
                serializer = LeadAssignSerializer(
                    data={
                        'lead_id':        lead_id,
                        'assigned_to_id': assigned_to_id,
                        'notes':          notes,
                    },
                    context={'request': request},
                )

                if serializer.is_valid():
                    lead            = serializer.validated_data['lead']
                    assignee        = serializer.validated_data['assignee']
                    assignment_type = serializer.validated_data['assignment_type']

                    if assignment_type == 'PRIMARY':
                        lead.assigned_to       = assignee
                        lead.assigned_by       = user
                        lead.assigned_date     = timezone.now()
                        lead.sub_assigned_to   = None
                        lead.sub_assigned_by   = None
                        lead.sub_assigned_date = None
                    elif assignment_type == 'SUB':
                        lead.sub_assigned_to   = assignee
                        lead.sub_assigned_by   = user
                        lead.sub_assigned_date = timezone.now()

                    lead.save()

                    LeadAssignment.objects.create(
                        lead=lead,
                        assigned_to=assignee,
                        assigned_by=user,
                        assignment_type=assignment_type,
                        notes=notes,
                    )
                    success_count += 1

                    if assignee == user:
                        continue

                    uid = assignee.id
                    if uid not in assigned_summary:
                        assigned_summary[uid] = {
                            'user':  assignee,
                            'leads': [],
                            'type':  assignment_type,
                        }
                    assigned_summary[uid]['leads'].append({
                        'lead_id':   lead.id,
                        'lead_name': lead.name,
                        'priority':  lead.priority,
                    })

                else:
                    failed_leads.append({'lead_id': lead_id, 'errors': serializer.errors})

            except Exception as e:
                failed_leads.append({'lead_id': lead_id, 'error': str(e)})

        # 🔔 One grouped Pusher notification per assignee (self-assignments already excluded above)
        for uid, summary in assigned_summary.items():
            count = len(summary['leads'])
            trigger_pusher(
                channel=f'private-user-{uid}',
                event='lead.assigned',
                data={
                    'bulk':             True,
                    'count':            count,
                    'leads':            summary['leads'],
                    'assignment_type':  summary['type'],
                    'assigned_by_id':   user.id,
                    'assigned_by_name': user.get_full_name() or user.username,
                    'message': (
                        f"{count} lead{'s' if count > 1 else ''} assigned to you "
                        f"by {user.get_full_name() or user.username}"
                    ),
                }
            )

        return Response({
            'message':       f'Successfully assigned {success_count} leads',
            'success_count': success_count,
            'failed_count':  len(failed_leads),
            'failed_leads':  failed_leads,
        }, status=status.HTTP_200_OK)


# ── Lead Assignment History View
class LeadAssignmentHistoryView(generics.ListAPIView):
    serializer_class   = LeadAssignmentSerializer
    permission_classes = [CanAccessLeads]

    def get_queryset(self):
        lead_id = self.kwargs.get('lead_id')
        lead    = get_object_or_404(Lead, id=lead_id)
        user    = self.request.user

        if user.role in FULL_ACCESS_ROLES:
            return LeadAssignment.objects.filter(lead=lead).order_by('-timestamp')

        if lead.assigned_to != user and lead.sub_assigned_to != user:
            return LeadAssignment.objects.none()

        return LeadAssignment.objects.filter(lead=lead).order_by('-timestamp')


# ── My Team Leads View
class MyTeamLeadsView(generics.ListAPIView):
    serializer_class   = LeadListSerializer
    permission_classes = [CanAccessLeads]
    pagination_class   = LeadPagination

    def get_queryset(self):
        user = self.request.user
        base_qs = Lead.objects.select_related(
            'assigned_to', 'assigned_by',
            'sub_assigned_to', 'sub_assigned_by',
        )
        if user.role in FULL_ACCESS_ROLES:
            return base_qs.all().distinct()
        return base_qs.filter(
            models.Q(assigned_to=user) |
            models.Q(sub_assigned_to=user)
        ).distinct()


# ── Available Users for Assignment
class AvailableUsersForAssignmentView(APIView):
    permission_classes = [CanAssignLeads]

    def get(self, request):
        ASSIGNABLE_ROLES = [
            'OPS', 'ADM_MANAGER', 'ADM_EXEC',
            'CM', 'BDM', 'FOE', 'ADM_COUNSELLOR',
        ]
        users = User.objects.filter(
            role__in=ASSIGNABLE_ROLES,
            is_active=True,
        ).values(
            'id', 'username', 'email', 'role', 'first_name', 'last_name'
        ).order_by('role', 'first_name', 'last_name')

        return Response(list(users), status=status.HTTP_200_OK)


# ── Unassign Lead View
class UnassignLeadView(APIView):
    permission_classes = [CanAssignLeads]

    def post(self, request):
        lead_id       = request.data.get('lead_id')
        unassign_type = request.data.get('unassign_type', 'SUB')

        if not lead_id:
            return Response(
                {'error': 'lead_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return Response(
                {'error': 'Lead not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        if user.role == 'ADM_EXEC':
            return Response(
                {'error': 'Admission Executives cannot unassign leads'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if user.role in FULL_ACCESS_ROLES:
            if unassign_type == 'PRIMARY':
                lead.assigned_to       = None
                lead.assigned_by       = None
                lead.assigned_date     = None
                lead.sub_assigned_to   = None
                lead.sub_assigned_by   = None
                lead.sub_assigned_date = None
            elif unassign_type == 'SUB':
                lead.sub_assigned_to   = None
                lead.sub_assigned_by   = None
                lead.sub_assigned_date = None

        elif user.role == 'ADM_MANAGER':
            if lead.assigned_to != user:
                return Response(
                    {'error': 'You can only unassign leads assigned to you'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            lead.sub_assigned_to   = None
            lead.sub_assigned_by   = None
            lead.sub_assigned_date = None

        else:
            return Response(
                {'error': 'You do not have permission to unassign leads'},
                status=status.HTTP_403_FORBIDDEN,
            )

        lead.save()

        return Response({
            'message': 'Lead unassigned successfully',
            'lead':    LeadDetailSerializer(lead).data,
        }, status=status.HTTP_200_OK)


# ── Update Lead View
class UpdateLeadView(APIView):
    permission_classes = [CanAccessLeads]

    def patch(self, request, pk):
        lead = get_object_or_404(Lead, id=pk)

        if (
            lead.assigned_to != request.user
            and lead.sub_assigned_to != request.user
            and request.user.role not in FULL_ACCESS_ROLES
        ):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN,
            )

        old_status = lead.status

        serializer = LeadUpdateSerializer(
            lead,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        updated_lead = serializer.save()

        if old_status != 'CONVERTED' and updated_lead.status == 'CONVERTED':
            send_conversion_email(updated_lead)

        return Response(serializer.data, status=status.HTTP_200_OK)


# ── Bulk Lead Upload View
class BulkLeadUploadView(APIView):
    permission_classes = [CanAccessLeads]
    parser_classes     = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if file.size > 5 * 1024 * 1024:
            return Response({'error': 'File too large (max 5MB)'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
        except Exception:
            return Response({'error': 'Invalid Excel file'}, status=status.HTTP_400_BAD_REQUEST)

        required_columns = ['name', 'phone', 'assigned_to']
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            return Response(
                {'error': f'Missing required columns: {missing_cols}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_map = {
            user.username.lower(): user
            for user in User.objects.filter(is_active=True)
        }

        success_count    = 0
        failed_rows      = []
        assigned_summary = {}

        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    name       = clean_value(row.get('name'))
                    email      = clean_value(row.get('email'))
                    source     = clean_value(row.get('source'))
                    status_val = clean_value(row.get('status'))
                    priority   = clean_value(row.get('priority'))
                    program    = clean_value(row.get('program'))
                    location   = clean_value(row.get('location'))
                    username   = clean_value(row.get('assigned_to'))

                    phone = clean_value(row.get('phone'))
                    if phone:
                        phone = str(phone).split('.')[0]

                    if not username:
                        failed_rows.append({'row': index + 2, 'error': 'assigned_to is required'})
                        continue

                    assignee_user = user_map.get(username.lower())
                    if not assignee_user:
                        failed_rows.append({
                            'row':   index + 2,
                            'error': f"User '{username}' not found",
                        })
                        continue

                    data = {
                        'name':        name,
                        'phone':       phone,
                        'email':       email,
                        'status':      str(status_val).upper() if status_val else 'ENQUIRY',
                        'priority':    str(priority).upper()   if priority   else 'MEDIUM',
                        'program':     program,
                        'location':    location,
                        'assigned_to': username,
                    }
                    if source:
                        data['source'] = str(source).upper()

                    serializer = BulkLeadCreateSerializer(
                        data=data,
                        context={'request': request, 'user_map': user_map},
                    )

                    if serializer.is_valid():
                        lead = serializer.save()
                        success_count += 1

                        #  FIX: skip notification summary if uploader assigned to themselves
                        if assignee_user == request.user:
                            continue

                        uid = assignee_user.id
                        if uid not in assigned_summary:
                            assigned_summary[uid] = {
                                'user':  assignee_user,
                                'leads': [],
                            }
                        assigned_summary[uid]['leads'].append({
                            'lead_id':   lead.id,
                            'lead_name': lead.name,
                            'priority':  lead.priority,
                        })

                    else:
                        failed_rows.append({
                            'row':    index + 2,
                            'data':   data,
                            'errors': serializer.errors,
                        })

                except Exception as e:
                    failed_rows.append({'row': index + 2, 'error': str(e)})

        # 🔔 One grouped Pusher notification per assignee (self-assignments already excluded above)
        for uid, summary in assigned_summary.items():
            count = len(summary['leads'])
            trigger_pusher(
                channel=f'private-user-{uid}',
                event='lead.assigned',
                data={
                    'bulk':             True,
                    'count':            count,
                    'leads':            summary['leads'],
                    'assignment_type':  'PRIMARY',
                    'assigned_by_id':   request.user.id,
                    'assigned_by_name': request.user.get_full_name() or request.user.username,
                    'message': (
                        f"{count} new lead{'s' if count > 1 else ''} uploaded and "
                        f"assigned to you by {request.user.get_full_name() or request.user.username}"
                    ),
                }
            )

        return Response({
            'message':       'Bulk upload completed',
            'success_count': success_count,
            'failed_count':  len(failed_rows),
            'failed_rows':   failed_rows,
        }, status=status.HTTP_200_OK)


# ── Today's Leads
class TodayLeadsAPI(APIView):
    permission_classes = [CanAccessLeads]

    def get(self, request):
        today = date.today()
        leads = Lead.objects.filter(
            created_at__date=today
        ).values('id', 'name', 'status', 'assigned_to')
        return Response(list(leads))