from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

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