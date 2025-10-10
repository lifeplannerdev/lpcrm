from django import forms
from .models import DailyReport

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['name', 'heading', 'report_text']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Monday Progress Report, Weekly Summary',
                'class': 'form-control'
            }),
            'heading': forms.TextInput(attrs={
                'placeholder': 'Brief summary of your daily achievements',
                'class': 'form-control'
            }),
            'report_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Detailed description of your daily work, achievements, and plans...',
                'class': 'form-control'
            }),
        }