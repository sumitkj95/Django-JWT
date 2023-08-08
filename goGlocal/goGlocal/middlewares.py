from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request
from rest_framework_simplejwt import authentication as jwt_auth


def get_user_jwt(request):
    user = None
    try:
        user_jwt = jwt_auth.JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except:
        pass

    return user


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        request = self.process_request(request)
        response = self.get_response(request)

        return response

    def process_request(self, request):
        request.user = SimpleLazyObject(lambda : get_user_jwt(request))

