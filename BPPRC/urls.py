from django.contrib import admin
from django.conf.urls.static import static, settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
