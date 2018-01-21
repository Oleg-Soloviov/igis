from django.urls import re_path, path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  re_path(r'^admin/', admin.site.urls),

  re_path(r'^', include('igis_udm.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
