from goGlocal.views import UserProfileView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path

from .swagger import schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('playground/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', lambda request: redirect('playground/', permanent=False)),
    path('accounts/login/', lambda request: redirect('/admin/', permanent=False))
]
