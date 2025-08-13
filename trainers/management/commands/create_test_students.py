from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from trainers.models import Trainer, Student
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test students for trainer'

    def handle(self, *args, **options):
        # Create trainer user if it doesn't exist
        trainer_user, created = User.objects.get_or_create(
            username='trainer',
            defaults={
                'first_name': 'Test',
                'last_name': 'Trainer',
                'role': 'TRAINER',
                'is_active': True
            }
        )
        
        if created:
            trainer_user.set_password('trainer123')
            trainer_user.save()
            self.stdout.write(self.style.SUCCESS('Created trainer user'))
        
        # Get or create trainer profile
        trainer, created = Trainer.objects.get_or_create(user=trainer_user)
        if created:
            self.stdout.write(self.style.SUCCESS('Created trainer profile'))
        
        # Create some test students
        students_data = [
            {'name': 'John Doe', 'batch': 'A1', 'status': 'ACTIVE', 'notes': 'Good progress'},
            {'name': 'Jane Smith', 'batch': 'A2', 'status': 'ACTIVE', 'notes': 'Needs more practice'},
            {'name': 'Mike Johnson', 'batch': 'B1', 'status': 'PAUSED', 'notes': 'On vacation'},
            {'name': 'Sarah Wilson', 'batch': 'B2', 'status': 'COMPLETED', 'notes': 'Excellent performance'},
            {'name': 'Tom Brown', 'batch': 'A1', 'status': 'ACTIVE', 'notes': ''},
        ]
        
        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                name=student_data['name'],
                trainer=trainer,
                defaults={
                    'batch': student_data['batch'],
                    'status': student_data['status'],
                    'notes': student_data['notes'],
                    'admission_date': date.today()
                }
            )
            if created:
                self.stdout.write(f'Created student: {student.name}')
        
        self.stdout.write(self.style.SUCCESS('Test students created successfully!')) 