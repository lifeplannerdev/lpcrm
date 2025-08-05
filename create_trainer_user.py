#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lpcrm.settings')
django.setup()

from accounts.models import User

def create_trainer_user():
    """Create a trainer user for testing"""
    try:
        # Check if trainer user already exists
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
            print("✅ Successfully created trainer user")
            print("Username: trainer")
            print("Password: trainer123")
        else:
            # Update password if user exists
            trainer.set_password('trainer123')
            trainer.save()
            print("✅ Trainer user already exists, password updated")
            print("Username: trainer")
            print("Password: trainer123")
            
    except Exception as e:
        print(f"❌ Error creating trainer user: {e}")

if __name__ == '__main__':
    create_trainer_user() 