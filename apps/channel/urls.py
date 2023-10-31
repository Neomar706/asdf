from django.urls import path
from .views import channel_view, add_video, get_videos_of_channel, toggle_suscriber, add_playlist

app_name = 'channel'

urlpatterns = [
    path('@<user>/<tab>/', channel_view, name='main'),
    path('add-video/', add_video, name='add-video'),
    path('add-playlist/', add_playlist, name='add-playlist'),
    path('@<user>/get-videos/<filter>/', get_videos_of_channel, name='get-videos'),
    path('add-suscriber/<user>/', toggle_suscriber, name='toggle-suscriber'),
]
