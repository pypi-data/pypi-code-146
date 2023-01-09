from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Session authentication class without CSRF token validation"""

    def enforce_csrf(self, request):
        return
