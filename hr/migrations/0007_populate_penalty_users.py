from django.db import migrations
from django.conf import settings

def populate_users(apps, schema_editor):
    Penalty = apps.get_model('hr', 'Penalty')
    # Get the User model - adjust 'accounts' to your actual auth app name
    User = apps.get_model('accounts', 'User')  # Change 'accounts' if your auth app is different
    
    # Assign to a default user (first user in database)
    default_user = User.objects.first()
    if default_user:
        Penalty.objects.filter(user__isnull=True).update(user=default_user)
    else:
        # If no users exist, delete penalties without users
        Penalty.objects.filter(user__isnull=True).delete()

def reverse_populate(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('hr', '0006_remove_penalty_employee_alter_penalty_options_and_more'),
        ('accounts', '__first__'),  # Change 'accounts' to your auth app name
    ]

    operations = [
        migrations.RunPython(populate_users, reverse_populate),
    ]