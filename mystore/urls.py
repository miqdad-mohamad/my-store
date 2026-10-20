from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os


admin_url = os.environ.get('ADMIN_URL', 'admin')

urlpatterns = [
    path(admin_url, admin.site.urls),
    path('', include('store.urls')),
    path('api/', include('store.api_urls')),
]

# Serve user-uploaded media files only during local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
