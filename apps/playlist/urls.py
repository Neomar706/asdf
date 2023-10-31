from django.urls import path
from .views import add_playlist, add_videos_to_playlist, edit_playlist, remove_playlist

app_name = 'playlist'


urlpatterns = [
    path('add-playlist/', add_playlist, name='add-playlist'),
    path('add-videos-to-playlist/<playlist>/', add_videos_to_playlist, name='add-videos-to-playlist'),
    path('edit-playlist/<playlist>/', edit_playlist, name='edit-playlist'),
    path('remove-playlist/<playlist>/', remove_playlist, name='remove-playlist')
]
