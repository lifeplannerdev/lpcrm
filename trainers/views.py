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

@login_required
def trainer_dashboard(request):
    # Check if user has trainer role
    if request.user.role != 'TRAINER':
        return redirect('accounts:landing')
    
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
    total_students = students.count()
    active_students = students.filter(status='ACTIVE').count()
    paused_students = students.filter(status='PAUSED').count()
    completed_students = students.filter(status='COMPLETED').count()
    
    # Get tasks assigned by this trainer
    assigned_tasks = Task.objects.filter(assigned_by=request.user).order_by('-priority', '-created_at')
    
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
    
    return render(request, 'trainers/student_details.html', {
        'student': student,
        'trainer': trainer
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
        ).order_by('batch', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update({
            'active_count': queryset.filter(status='ACTIVE').count(),
            'paused_count': queryset.filter(status='PAUSED').count(),
            'completed_count': queryset.filter(status='COMPLETED').count()
        })
        return context