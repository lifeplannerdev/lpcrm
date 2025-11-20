from django import forms
from .models import Student
from django.core.validators import MinLengthValidator

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'batch', 'status', 'admission_date','email', 'phone_number', 'drive_link', 'student_class','notes']
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
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student phone number'
            }),
            'drive_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Google Drive link'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes about the student...',
                'rows': 3
            }),
            'student_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student class'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(MinLengthValidator(3))
        # Set default admission date to today
        if not self.instance.pk:
            self.fields['admission_date'].initial = forms.DateField().initial



from django import forms
from .models import Attendance, Student

class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students', [])
        date = kwargs.pop('date', None)
        super().__init__(*args, **kwargs)
        
        for student in students:
            # Get existing attendance for this date if any
            initial_status = 'PRESENT'
            if date:
                try:
                    existing_attendance = Attendance.objects.get(
                        date=date, 
                        student=student
                    )
                    initial_status = existing_attendance.status
                except Attendance.DoesNotExist:
                    pass
            
            self.fields[f'student_{student.id}'] = forms.ChoiceField(
                choices=[
                    ('PRESENT', 'Present'),
                    ('ABSENT', 'Absent'), 
                    ('NO_SESSION', 'No Session')
                ],
                initial=initial_status,
                widget=forms.RadioSelect(attrs={
                    'class': 'attendance-radio',
                    'data-student-id': str(student.id)
                }),
                label=f"{student.name} ({student.get_batch_display()})"
            )            