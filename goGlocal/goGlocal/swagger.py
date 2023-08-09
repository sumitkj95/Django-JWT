from drf_yasg import openapi, generators
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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


class CustomSchemaGenerator(generators.SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)

        # Add security requirements (JWT token)
        security = [{}]
        if request and request.user and request.user.is_authenticated:
            security = [{"Bearer": []}]
        schema.security = security

        return schema
