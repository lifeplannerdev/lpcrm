import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # change this
django.setup()

from leads.models import Lead  # change app name if different
from django.db.models import Count

dupes = (
    Lead.objects
    .values('phone')
    .annotate(count=Count('id'))
    .filter(count__gt=1)
    .order_by('-count')
)

total_dupe_groups  = dupes.count()
total_dupe_records = sum(d['count'] for d in dupes)

print(f"Total leads            : {Lead.objects.count()}")
print(f"Duplicate phone groups : {total_dupe_groups}")
print(f"Records in those groups: {total_dupe_records}")
print(f"Extra records to clean : {total_dupe_records - total_dupe_groups}")
print()

for d in dupes:
    leads = Lead.objects.filter(phone=d['phone']).values(
        'id', 'name', 'status', 'assigned_to__username', 'created_at'
    )
    print(f"--- {d['phone']} ({d['count']} records) ---")
    for l in leads:
        print(f"  id={l['id']}  name={l['name']}  status={l['status']}  assigned={l['assigned_to__username']}  created={l['created_at']:%Y-%m-%d}")
    print()