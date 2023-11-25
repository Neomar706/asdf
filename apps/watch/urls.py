from django.urls import path
from .views import watch_video, toggle_like, create_comment, toggle_like_comment


app_name = 'watch'

urlpatterns = [
    path('<pk>/', watch_video, name='watch-video'),
    path('toggle-like/<video>/', toggle_like, name='toggle-like'),
    path('toggle-likes/<comment>/', toggle_like_comment, name='toggle-like-comment'),
    path('create-comment/<video>/<issuer_channel>/', create_comment, name='create-comment')
]
