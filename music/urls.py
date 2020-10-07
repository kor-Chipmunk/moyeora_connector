from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('songs', views.list_create_songs),
    path('songs/my', views.get_my_songs),

    path('songs/<int:song_id>', views.retrieve_put_delete_song),

    path('play', views.song_play),
    path('next', views.song_next),
    path('prev', views.song_prev),
    path('clear', views.song_clear),

    path('songs/history', views.get_history),
    path('songs/history/my', views.get_my_history),
    path('songs/history/<int:song_id>', views.get_history_song),

    path('songs/<int:song_id>/comments', views.list_create_comments),

    path('songs/<int:song_id>/comments/<int:comment_id>', views.retrieve_put_delete_comment),

    path('songs/<int:song_id>/like', views.post_like),
])