from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # mediaを使うために追加
from . import settings
from django.shortcuts import redirect


def redirect_to_home(request):
    return redirect('/siniagram/home/1/')


urlpatterns = [
    path('', redirect_to_home),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('siniagram/', include('snsapp.urls')),
    path('', include('pwa.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)  # 追加
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
