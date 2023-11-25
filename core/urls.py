from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', HomeView.as_view(), name='home-view'),
    path('account/', include('allauth.urls')),
    path('channel/', include('apps.channel.urls', namespace='channel')),
    path('playlist/', include('apps.playlist.urls', namespace='playlist')),
    path('watch/', include('apps.watch.urls', namespace='watch'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
