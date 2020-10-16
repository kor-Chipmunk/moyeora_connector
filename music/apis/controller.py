from datetime import timedelta

from django.core.cache import cache
from django.db.models import Count, Sum, F, OuterRef, Subquery
from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend, filters
from requests import Response
from rest_framework import (
    authentication,
    status,
)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from moyeora_connector.exception_handler import CommonAPIException
from moyeora_connector.responses import CommonResponse

from ..models import (
    Song
)
from ..serializers import (
    SongSerializer,
)

__all__ = (
    "song_play",
    "song_clear",
)

from ..tasks import play_song

@api_view(["POST"])
@permission_classes([IsAdminUser])
def song_play(request):
    songs = Song.objects.filter(is_played=False) \
        .order_by('-count_likes') \
        .select_related('user')

    if not songs:
        raise CommonAPIException('MUSIC_SONG_PLAY_EMPTY', status.HTTP_200_OK, "신청곡 대기열이 비어있습니다!")

    original_song = songs[0]
    unplayed_songs = songs.values()[0]
    unplayed_songs['is_played'] = True

    serializer = SongSerializer(original_song, data=unplayed_songs, partial=True)
    serializer.is_valid(raise_exception=True)

    song_url = play_song(serializer.validated_data['title'], serializer.validated_data['url'])
    serializer.validated_data['url'] = song_url

    serializer.save()
    return CommonResponse('MUSIC_PLAY_SUCCESS', status.HTTP_200_OK, serializer.data, '성공적으로 노래를 재생했습니다.')

@api_view(["POST"])
@permission_classes([IsAdminUser])
def song_clear(request):
    unplayed_songs = Song.objects.prefetch_related('user').filter(is_played=False)
    unplayed_songs.delete()

    return CommonResponse('MUSIC_SONG_CLEAR', status.HTTP_204_NO_CONTENT, True, '신청곡 목록을 모두 삭제했습니다.')