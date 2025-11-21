from typing import Any


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .models import Trainer, Student
from .forms import StudentForm
from tasks.models import Task
from django.utils import timezone
from .models import Attendance
from .forms import AttendanceForm
from datetime import date, timedelta


@login_required
def trainer_dashboard(request):
    # Check if user has trainer role
    if request.user.role != 'TRAINER':
        return redirect('accounts:landing')
    
    Task.update_overdue_tasks()
    # Get or create trainer profile
    trainer, created = Trainer.objects.get_or_create(user=request.user)
    
    students = trainer.students.all().order_by('batch', 'name')
    
    # Group students by batch
    batches = {
        'A1': students.filter(batch='A1'),
        'A2': students.filter(batch='A2'), 
        'B1': students.filter(batch='B1'),
        'B2': students.filter(batch='B2')
    }
    
    # Calculate stats for the dashboard
    total_students: Any = students.count()
    active_students = students.filter(status='ACTIVE').count()
    paused_students = students.filter(status='PAUSED').count()
    completed_students = students.filter(status='COMPLETED').count()
    
    # Get tasks assigned to this trainer
    assigned_tasks = Task.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    
    # Create form instance for the modal
    form = StudentForm()
    
    return render(request, 'trainers/dashboard.html', {
        'trainer': trainer,
        'batches': batches,
        'all_students': students,  # Added for the table
        'total_students': total_students,
        'active_students': active_students,
        'paused_students': paused_students,
        'completed_students': completed_students,
        'assigned_tasks': assigned_tasks,  # Added for task listing
        'form': form
    })

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_task_status(request, task_id):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        new_status = data.get('status')
        
        print(f"Updating task {task_id} to status: {new_status}")  # Debug log
        
        # Get the task and verify the user is assigned to it
        task = get_object_or_404(
            Task,
            id=task_id,
            assigned_to=request.user
        )
        
        # Validate the status
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid status: {new_status}'
            }, status=400)
        
        # Update the status
        task.status = new_status
        if new_status == 'completed':
            task.mark_completed()
        else:
            task.completed_at = None  # Reset completed date if status changed from completed
            task.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Task status updated successfully',
            'task': {
                'status': task.status,
                'status_display': task.get_status_display(),
                'completed_at': task.completed_at.strftime('%b %d, %Y %I:%M %p') if task.completed_at else None
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Error updating task status: {str(e)}")  # Debug log
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400) 

@login_required
@require_http_methods(["POST"])
@csrf_exempt  # Only if you're having CSRF issues with AJAX
def update_student_notes(request):
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        notes = data.get('notes', '')
        
        # Verify the student belongs to the requesting trainer
        student = get_object_or_404(
            Student,
            id=student_id,
            trainer__user=request.user
        )
        
        student.notes = notes
        student.save()
        
        return JsonResponse({
            'status': 'success',
            'notes': student.notes,
            'truncated_notes': student.notes[:50] + '...' if len(student.notes) > 50 else student.notes
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def add_student(request):
    if request.user.role != 'TRAINER':
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        trainer = Trainer.objects.get(user=request.user)
        form = StudentForm(request.POST)
        
        if form.is_valid():
            student = form.save(commit=False)
            student.trainer = trainer
            student.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Student added successfully',
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'batch': student.get_batch_display(),
                    'status': student.get_status_display(),
                    'admission_date': student.admission_date.strftime('%b %d, %Y'),
                    'notes': student.notes,
                    'email': student.email or '',
                    'phone_number': student.phone_number or '',
                    'drive_link': student.drive_link or '',
                    'student_class': student.get_student_class_display() if student.student_class else ''
                }
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
@require_http_methods(["POST"])
def edit_student(request, student_id):
    if request.user.role != 'TRAINER':
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        # Verify the student belongs to the requesting trainer
        student = get_object_or_404(
            Student,
            id=student_id,
            trainer__user=request.user
        )
        
        form = StudentForm(request.POST, instance=student)
        
        if form.is_valid():
            student = form.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Student updated successfully',
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'batch': student.get_batch_display(),
                    'status': student.get_status_display(),
                    'admission_date': student.admission_date.strftime('%b %d, %Y'),
                    'notes': student.notes,
                    'email': student.email or '',
                    'phone_number': student.phone_number or '',
                    'drive_link': student.drive_link or '',
                    'student_class': student.get_student_class_display() if student.student_class else ''
                }
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
@require_http_methods(["POST"])
def delete_student(request):
    if request.user.role != 'TRAINER':
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        
        # Verify the student belongs to the requesting trainer
        student = get_object_or_404(
            Student,
            id=student_id,
            trainer__user=request.user
        )
        
        # Store student name for response message before deletion
        student_name = student.name
        
        # Delete the student
        student.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Student {student_name} deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
@require_http_methods(["GET", "POST"])
def delete_student2(request, student_id):
    if request.user.role != 'TRAINER':
        messages.error(request, 'Unauthorized')
        return redirect('trainers:student_list')
    
    # Verify the student belongs to the requesting trainer
    student = get_object_or_404(
        Student,
        id=student_id,
        trainer__user=request.user
    )
    
    if request.method == 'POST':
        try:
            # Store student name for response message before deletion
            student_name = student.name
            
            # Delete the student
            student.delete()
            
            messages.success(request, f'Student {student_name} deleted successfully')
            return redirect('trainers:student_list')
        except Exception as e:
            messages.error(request, f'Error deleting student: {str(e)}')
            return redirect('trainers:student_list')
    else:
        # For GET requests, show confirmation page or redirect back
        messages.warning(request, f'Please confirm deletion of student {student.name}')
        return redirect('trainers:student_details', student_id=student_id)

@login_required
@require_http_methods(["GET"])
def student_details(request, student_id):
    # Check if user has trainer role
    if request.user.role != 'TRAINER':
        return redirect('accounts:landing')
    
    # Get or create trainer profile
    trainer, created = Trainer.objects.get_or_create(user=request.user)
    
    # Verify the student belongs to the requesting trainer
    student = get_object_or_404(
        Student,
        id=student_id,
        trainer=trainer
    )
    
    # Get attendance records for this student using the Attendance model
    # This ensures we're actually querying the database for attendance data
    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by('-date', '-marked_at')
    
    return render(request, 'trainers/student_details.html', {
        'student': student,
        'trainer': trainer,
        'attendance_records': attendance_records  
    })

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'trainers/student_list.html'
    context_object_name = 'students'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has trainer role
        if request.user.role != 'TRAINER':
            return redirect('accounts:landing')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        # Get or create trainer profile
        trainer, created = Trainer.objects.get_or_create(user=self.request.user)
        return Student.objects.filter(
            trainer=trainer
        ).order_by('-admission_date', 'batch', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update({
            'active_count': queryset.filter(status='ACTIVE').count(),
            'paused_count': queryset.filter(status='PAUSED').count(),
            'completed_count': queryset.filter(status='COMPLETED').count()
        })
        return context


@login_required
def attendance_view(request):
    if request.user.role != 'TRAINER':
        return redirect('accounts:landing')
    
    trainer = Trainer.objects.get(user=request.user)
    students = trainer.students.filter(status='ACTIVE').order_by('batch', 'name')
    today = timezone.now().date()
    
    # Get attendance history (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    attendance_dates = Attendance.objects.filter(
        trainer=trainer,
        date__gte=thirty_days_ago
    ).values('date').distinct().order_by('-date')
    
    # Prepare initial data for today's attendance
    initial_data = {}
    for student in students:
        field_name = f'student_{student.id}'
        try:
            # Get existing attendance for today
            existing_attendance = Attendance.objects.get(
                date=today,
                trainer=trainer,
                student=student
            )
            initial_data[field_name] = existing_attendance.status
        except Attendance.DoesNotExist:
            initial_data[field_name] = 'PRESENT'  # Default to present
    
    if request.method == 'POST':
        # Process attendance form
        attendance_date = request.POST.get('attendance_date', today)
        
        try:
            if isinstance(attendance_date, str):
                attendance_date = date.fromisoformat(attendance_date)
        except ValueError:
            attendance_date = today
        
        attendance_count = 0
        for student in students:
            status_key = f'student_{student.id}'
            status = request.POST.get(status_key)
            
            if status in ['PRESENT', 'ABSENT', 'NO_SESSION']:
                Attendance.objects.update_or_create(
                    date=attendance_date,
                    trainer=trainer,
                    student=student,
                    defaults={'status': status}
                )
                attendance_count += 1
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'Attendance marked for {attendance_count} students!'
            })
        else:
            messages.success(request, f'Attendance marked for {attendance_count} students!')
            return redirect('trainers:attendance')
    
    return render(request, 'trainers/attendance.html', {
        'trainer': trainer,
        'students': students,
        'today': today,
        'initial_data': initial_data,  # Pass initial data directly
        'attendance_dates': attendance_dates
    })

    
@login_required
def get_attendance_detail(request):
    """AJAX view to get attendance details for modal"""
    if request.user.role != 'TRAINER':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter required'}, status=400)
    
    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    trainer = Trainer.objects.get(user=request.user)
    
    # Get attendance records for the specific date
    attendance_records = Attendance.objects.filter(
        trainer=trainer,
        date=target_date
    ).select_related('student').order_by('student__batch', 'student__name')
    
    # Count statistics
    present_count = attendance_records.filter(status='PRESENT').count()
    absent_count = attendance_records.filter(status='ABSENT').count()
    no_session_count = attendance_records.filter(status='NO_SESSION').count()
    total_count = present_count + absent_count + no_session_count
    
    # Prepare data for JSON response
    attendance_data = []
    for record in attendance_records:
        attendance_data.append({
            'student_name': record.student.name,
            'batch': record.student.get_batch_display(),
            'status': record.status,
            'status_display': record.get_status_display(),
            'marked_at': record.marked_at.strftime('%I:%M %p') if record.marked_at else 'N/A'
        })
    
    return JsonResponse({
        'date': target_date.strftime('%B %d, %Y'),
        'attendance_data': attendance_data,
        'stats': {
            'present': present_count,
            'absent': absent_count,
            'no_session': no_session_count,
            'total': total_count
        }
    })

@login_required
def quick_mark_attendance(request):
    """Quick mark all students as present/absent/no_session"""
    if request.user.role != 'TRAINER':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')
        attendance_date = data.get('date')
        
        if status not in ['PRESENT', 'ABSENT', 'NO_SESSION']:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        try:
            if isinstance(attendance_date, str):
                attendance_date = date.fromisoformat(attendance_date)
        except ValueError:
            attendance_date = timezone.now().date()
        
        trainer = Trainer.objects.get(user=request.user)
        students = trainer.students.filter(status='ACTIVE')
        
        attendance_count = 0
        for student in students:
            Attendance.objects.update_or_create(
                date=attendance_date,
                trainer=trainer,
                student=student,
                defaults={'status': status}
            )
            attendance_count += 1
        
        return JsonResponse({
            'status': 'success',
            'message': f'Marked all {attendance_count} students as {status.lower().replace("_", " ")}'
        })        