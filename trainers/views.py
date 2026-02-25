from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
import csv

from .models import Trainer, Student, Attendance
from .serializers import (
    TrainerSerializer, 
    StudentSerializer, 
    AttendanceSerializer,
    TrainerUserSerializer
)
from .permissions import IsTrainerOwnStudent

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100



class TrainerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Trainer.objects.select_related('user')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = TrainerSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TrainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        return Response(TrainerSerializer(trainer).data)

    def put(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        serializer = TrainerSerializer(trainer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        trainer.delete()
        return Response(status=204)


class TrainerUserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainers = User.objects.filter(role='TRAINER', is_active=True)
        
        search = request.GET.get('search')
        if search:
            trainers = trainers.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )
        
        serializer = TrainerUserSerializer(trainers.order_by('first_name'), many=True)
        return Response({
            'count': trainers.count(),
            'results': serializer.data
        })


class StudentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Student.objects.select_related('trainer', 'trainer__user')

        if hasattr(request.user, 'trainer_profile'):
            qs = qs.filter(trainer=request.user.trainer_profile)

        status_filter = request.GET.get('status')
        batch_filter = request.GET.get('batch')
        trainer_filter = request.GET.get('trainer')
        search = request.GET.get('search')

        if status_filter:
            qs = qs.filter(status=status_filter)
        if batch_filter:
            qs = qs.filter(batch=batch_filter)
        if trainer_filter:
            qs = qs.filter(trainer_id=trainer_filter)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = StudentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StudentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTrainerOwnStudent]

    def get_object(self, request, pk):
        qs = Student.objects.select_related('trainer', 'trainer__user')
        if hasattr(request.user, 'trainer_profile'):
            qs = qs.filter(trainer=request.user.trainer_profile)
        return get_object_or_404(qs, pk=pk)

    def get(self, request, pk):
        student = self.get_object(request, pk)
        return Response(StudentSerializer(student).data)

    def put(self, request, pk):
        student = self.get_object(request, pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        student = self.get_object(request, pk)
        student.delete()
        return Response(
            {"message": "Student deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )



class AttendanceListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Attendance.objects.select_related(
            'student', 'trainer', 'trainer__user'
        )

        if hasattr(request.user, 'trainer_profile'):
            qs = qs.filter(trainer=request.user.trainer_profile)

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = AttendanceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):  
        if not hasattr(request.user, 'trainer_profile'):
            return Response(
                {"detail": "Only trainers can mark attendance"},
                status=403
            )

        trainer = request.user.trainer_profile
        student_id = request.data.get('student')

        student = Student.objects.filter(
            id=student_id, trainer=trainer
        ).first()
        
        if not student:
            return Response(
                {"detail": "You can mark attendance only for your students"},
                status=403
            )

        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(trainer=trainer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        

class AttendanceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = Attendance.objects.select_related(
            'student', 'trainer', 'trainer__user'
        )

        if hasattr(request.user, 'trainer_profile'):
            records = records.filter(trainer=request.user.trainer_profile)

        student_id = request.GET.get('student')
        trainer_id = request.GET.get('trainer')
        date = request.GET.get('date')

        if student_id:
            records = records.filter(student_id=student_id)
        if trainer_id:
            records = records.filter(trainer_id=trainer_id)
        if date:
            records = records.filter(date=date)

        
        if date:
            serializer = AttendanceSerializer(records, many=True)
            return Response({
                'count': records.count(),
                'results': serializer.data
            })
        
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(records, request)
        serializer = AttendanceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class QuickMarkAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, 'trainer_profile'):
            return Response({"error": "Only trainers allowed"}, status=403)

        trainer = request.user.trainer_profile
        date = request.data.get('date')
        records = request.data.get('records', [])

        if not date or not records:
            return Response({"error": "date and records required"}, status=400)

        saved = []
        errors = []

        for r in records:
            try:
                student_id = r.get('student')
                student = Student.objects.filter(
                    id=student_id,
                    trainer=trainer
                ).exclude(status='COMPLETED').first()
                
                if not student:
                    continue

                obj, created = Attendance.objects.update_or_create(
                    student=student, 
                    date=date,
                    defaults={
                        'trainer': trainer,
                        'status': r.get('status', 'PRESENT')
                    }
                )
                saved.append(obj)
                
            except Exception as e:
                errors.append({
                    'student_id': r.get('student'),
                    'error': str(e)
                })
                print(f"Error saving attendance for student {r.get('student')}: {str(e)}")
                continue

        if not saved:
            return Response({
                'error': 'No attendance records were saved',
                'details': errors
            }, status=400)

        return Response(
            AttendanceSerializer(saved, many=True).data,
            status=201
        )


class AttendanceRecordsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        qs = Attendance.objects.filter(student_id=student_id)

        if hasattr(request.user, 'trainer_profile'):
            qs = qs.filter(trainer=request.user.trainer_profile)

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = AttendanceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExportStudentAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        qs = Attendance.objects.filter(student_id=student_id)

        if hasattr(request.user, 'trainer_profile'):
            qs = qs.filter(trainer=request.user.trainer_profile)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            f'attachment; filename="student_{student_id}_attendance.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(['Date', 'Trainer', 'Status'])

        for r in qs:
            writer.writerow([
                r.date,
                r.trainer.user.get_full_name(),
                r.status
            ])

        return response


class AttendanceStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'trainer_profile'):
            return Response(
                {"error": "Only trainers can access this endpoint"},
                status=403
            )

        trainer = request.user.trainer_profile
        
        students = Student.objects.filter(
            trainer=trainer
        ).exclude(
            status='COMPLETED'
        ).select_related('trainer', 'trainer__user').order_by('name')

        
        batch = request.GET.get('batch')
        student_class = request.GET.get('student_class')
        
        if batch:
            students = students.filter(batch=batch)
        if student_class:
            students = students.filter(student_class=student_class)

        serializer = StudentSerializer(students, many=True)
        return Response({
            'count': students.count(),
            'results': serializer.data
        })



class StudentStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Student.objects.all()
            
        if hasattr(request.user, 'trainer_profile'):
            qs = qs.filter(trainer=request.user.trainer_profile)
        
        stats = {
            "total": qs.count(),
            "ACTIVE": 0,
            "COMPLETED": 0,
            "PAUSED": 0,
            "DROPPED": 0,
        }

        for item in qs.values('status').annotate(c=Count('id')):
            stats[item['status']] = item['c']

        stats["PAUSED_DROPPED"] = stats["PAUSED"] + stats["DROPPED"]
        return Response(stats)
