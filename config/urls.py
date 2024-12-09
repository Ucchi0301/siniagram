from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # mediaを使うために追加
from . import settings
from django.shortcuts import redirect


urlpatterns = [
    path('', include('snsapp.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls'), name="accounts"),
    path('siniagram/', include('snsapp.urls')),
    path('', include('pwa.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
