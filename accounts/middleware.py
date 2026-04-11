from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from .utils import set_current_user

class AdminSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)  # Ensure session exists
        
        if hasattr(request, 'session'):  # Safety check
            if request.path.startswith('/admin'):
                request.session.cookie_name = settings.ADMIN_SESSION_COOKIE_NAME
                request.session.cookie_path = settings.ADMIN_SESSION_COOKIE_PATH
            else:
                request.session.cookie_name = settings.SESSION_COOKIE_NAME
                request.session.cookie_path = settings.SESSION_COOKIE_PATH

        response = self.get_response(request)
        return response



class CurrentUserMiddleware:
    """
    Stores the authenticated request user in thread-local storage
    so that signals (which have no access to request) can log the
    correct user via log_activity().
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            set_current_user(request.user)
        else:
            set_current_user(None)

        response = self.get_response(request)

        # Always clear after request to avoid user leaking between threads
        set_current_user(None)

        return response