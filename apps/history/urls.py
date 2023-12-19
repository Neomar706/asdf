from django.urls import path
from .views import history_view, clear_history, toggle_pause_history, remove_from_history

app_name = 'history'

urlpatterns = [
    path('', history_view, name='main'),
    path('clear/', clear_history, name='clear'),
    path('pause/', toggle_pause_history, name='toggle-pause'),
    path('remove/<pk>/', remove_from_history, name='remove'),
]
