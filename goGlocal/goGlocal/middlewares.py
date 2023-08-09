from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = None
        jwt_auth = JWTAuthentication()

        # Check if Authorization header contains a valid token
        if 'Authorization' in request.headers:
            token = jwt_auth.get_raw_token(request.headers['Authorization'])
            try:
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
            except Exception as e:
                pass  # Token is invalid or expired

        request.user = user or AnonymousUser()
        response = self.get_response(request)
        return response
