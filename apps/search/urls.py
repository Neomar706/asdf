from django.urls import path
from .views import search_videos

app_name = 'search'

urlpatterns = [
    path('results', search_videos, name='main')
]