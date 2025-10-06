from django import forms
from .models import Task, TaskUpdate
from accounts.models import User
from django.utils import timezone

class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(
            role__in=['MEDIA', 'ADM_MANAGER', 'ADM_EXEC'],
            is_active=True
        ).order_by('role', 'first_name'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
        })
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'priority', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task description',
                'rows': 4
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskUpdate
        fields = ['new_status', 'notes']
        widgets = {
            'new_status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add update notes (optional)',
                'rows': 3
            }),
        }