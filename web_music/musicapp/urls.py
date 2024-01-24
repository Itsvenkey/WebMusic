from django.urls import path
from .views import index,play_song

urlpatterns = [
    # ... other URL patterns ...
     path('', index, name=''),
     path('youtube-search/<str:video_id>',play_song, name='play-song'),
]