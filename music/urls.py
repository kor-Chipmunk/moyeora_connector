from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested.routers import NestedSimpleRouter

from .apis import (
    RequestSongViewSet,
    HistorySongViewSet,
    CommentViewSet,
    SongLikeViewSet,
    CommentLikeViewSet,
    song_play,
    song_clear,
)
from .apis.stats import SongStatisticsViewSet

router = DefaultRouter()
router.register(
    r'songs',
    RequestSongViewSet,
    basename='song'
)
router.register(
    r'history',
    HistorySongViewSet,
    basename='history'
)
router.register(
    r'stats',
    SongStatisticsViewSet,
    basename="stat"
)

comments_router = NestedSimpleRouter(
    router,
    r'songs',
    lookup='song'
)
comments_router.register(
    r'comments',
    CommentViewSet,
    basename="song-comments"
)

song_likes_router = NestedSimpleRouter(
    router,
    r'songs',
    lookup='song'
)
song_likes_router.register(
    r'like',
    SongLikeViewSet,
    basename='song-likes'
)

comments_like_router = NestedSimpleRouter(
    comments_router,
    r'comments',
    lookup='comment'
)
comments_like_router.register(
    r'like',
    CommentLikeViewSet,
    basename='comment-likes'
)

urlpatterns = format_suffix_patterns([
    path('play', song_play),
    path('clear', song_clear),
])

urlpatterns += router.urls
urlpatterns += comments_router.urls
urlpatterns += song_likes_router.urls
urlpatterns += comments_like_router.urls