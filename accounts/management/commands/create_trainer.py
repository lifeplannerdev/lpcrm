from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create a trainer user for testing'

    def handle(self, *args, **options):
        # Create trainer user if it doesn't exist
        trainer, created = User.objects.get_or_create(
            username='trainer',
            defaults={
                'first_name': 'Trainer',
                'last_name': 'User',
                'email': 'trainer@example.com',
                'role': 'TRAINER',
                'is_active': True,
                'is_staff': True
            }
        )
        
        if created:
            trainer.set_password('trainer123')
            trainer.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully created trainer user')
            )
            self.stdout.write('Username: trainer')
            self.stdout.write('Password: trainer123')
        else:
            self.stdout.write(
                self.style.WARNING('Trainer user already exists')
            ) 