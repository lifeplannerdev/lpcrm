from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name', 
            'phone', 
            'email', 
            'priority', 
            'status', 
            'program', 
            'location', 
            'source', 
            'remarks',
            'custom_source'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter program name'
            }),
            'source': forms.Select(attrs={'class': 'form-control'}),
            'custom_source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify custom source',
                'style': 'display: none;'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter remarks'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values
        self.fields['priority'].initial = 'MEDIUM'
        self.fields['status'].initial = 'ENQUIRY'
        self.fields['email'].required = False
        self.fields['location'].required = False
        self.fields['custom_source'].required = False