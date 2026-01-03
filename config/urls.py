# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from apps.common.views import HomeAPIView # Import the view
from drf_spectacular.utils import extend_schema

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # THE HOMEPAGE MANUAL
    path('', HomeAPIView.as_view(), name='home_manual'),

    # API Routes
    path('api/v1/common/', include('apps.common.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/profiles/', include('apps.profiles.urls')),
    path('api/v1/properties/', include('apps.properties.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/interactions/', include('apps.interactions.urls')),
    path('api/v1/finance/', include('apps.finance.urls')),
    
    # Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)