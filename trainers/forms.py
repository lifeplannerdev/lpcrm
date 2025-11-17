from django import forms
from .models import Student
from django.core.validators import MinLengthValidator

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'batch', 'status', 'admission_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name'
            }),
            'batch': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'admission_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(MinLengthValidator(3))
        # Set default admission date to today
        if not self.instance.pk:
            self.fields['admission_date'].initial = forms.DateField().initial