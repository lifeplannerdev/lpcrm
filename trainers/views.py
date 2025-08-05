from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Trainer, Student

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
    
    return render(request, 'trainers/dashboard.html', {
        'trainer': trainer,
        'batches': batches,
        'all_students': students,  # Added for the table
        'total_students': total_students,
        'active_students': active_students,
        'paused_students': paused_students,
        'completed_students': completed_students
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