"""goGlocal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from goGlocal.views import UserProfileView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.shortcuts import redirect


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# schema_view = get_swagger_view(title='GoGlocal API')


from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi, generators


class CustomSchemaGenerator(generators.SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # schema.basePath = "/api"  # Adjust this if your APIs have a different base URL

        # Add security requirements (JWT token)
        security = [{}]
        if request and request.user and request.user.is_authenticated:
            security = [{"Bearer": []}]
        schema.security = security

        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="GoGlocal APIs",
        default_version='v1',
        description="API Docs",
        contact=openapi.Contact(email="sumitjiyani95@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('playground/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', lambda request: redirect('playground/', permanent=False)),
    path('accounts/login/', lambda request: redirect('/admin/', permanent=True))
]



