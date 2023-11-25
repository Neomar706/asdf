from django.urls import path
from .views import channel_view, add_video, get_videos_of_channel, toggle_suscriber

app_name = 'channel'

urlpatterns = [
    path('@<user>/<tab>/', channel_view, name='main'),
    path('add-video/', add_video, name='add-video'),
    path('@<user>/get-videos/<filter>/', get_videos_of_channel, name='get-videos'),
    path('add-suscriber/<user>/', toggle_suscriber, name='toggle-suscriber'),
]
