"""
healthpilot URL Configuration

"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include

# from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Health Pilot API",
        default_version='v1',
        description="This is the Health Pilot API with all the end points.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="menilik.eshetu@singularitynet.io"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/',include('client.urls')),

    # We added url to swagger for home-page since it return error[Page not found (404)] if we did not specify apps names
    path('', schema_view.with_ui('swagger',         
         cache_timeout=0), name='schema-swagger-ui'),
    #path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    # path('__debug__/', include('debug_toolbar.urls')),
]
