from django.shortcuts import render
from accounts.models import DailyReport, User

def is_hr(user):
    """Check if user is business head or higher"""
    return user.role in ['HR']

@login_required
@user_passes_test(is_business_head)
def hob_dashboard(request):
    """Main HOB Dashboard"""
    context = get_dashboard_context(request)
    return render(request, 'hob/dashboard.html', context)

