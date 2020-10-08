from django.core.cache import cache
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from moyeora_connector.responses import CommonResponse
from .exceptions import *

from .models import *
from .serializers import *


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_create_songs(request):
    cache_key = 'songs'

    if request.method == "GET":
        songs = cache.get(cache_key)

        if not songs:
            songs = Song.objects.filter(is_played = False) \
                .annotate(count_likes=Count('likes')) \
                .order_by('-count_likes')\
                .select_related('user')\
                .prefetch_related('likes')
            cache.set(cache_key, songs, timeout=60 * 5)

        serializer = SongWithUserNicknameSerializer(songs, many=True)

        return CommonResponse('MUSIC_REQUEST_SONGS', status.HTTP_200_OK, serializer.data, "신청곡 목록을 불러왔습니다.")
    elif request.method == "POST":
        request.data['user'] = request.user.pk

        serializer = SongCreateSerializer(data=request.data)

        if serializer.is_valid():
            cache.delete(cache_key)
            serializer.save()

            serializer = SongWithoutUserSerializer(serializer.data)

            return CommonResponse('MUSIC_REQUEST_SONGS_CREATED', status.HTTP_201_CREATED, serializer.data, "성공적으로 신청곡이 대기열에 올라갔습니다.")
        return MUSIC_REQUEST_SONG_INVALID

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_songs(request):
    songs = Song.objects.filter(user__id = request.user.pk, is_played=False)\
        .annotate(count_likes=Count('likes'))\
        .order_by('-count_likes')\
        .select_related('user')
    serializer = SongWithUserNicknameSerializer(songs, many=True)

    return CommonResponse('MUSIC_REQUEST_SONGS_MY', status.HTTP_200_OK, serializer.data, "성공적으로 신청곡을 불러왔습니다.")

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_put_delete_song(request, song_id):
    cache_key = 'songs'

    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        return MUSIC_REQUEST_SONG_NOTFOUND

    if request.method == "GET":
        serializer = SongWithUserNicknameSerializer(song)
        return CommonResponse('MUSIC_REQUEST_SONGS_DETAIL', status.HTTP_200_OK, serializer.data, "성공적으로 해당 신청곡을 불러왔습니다.")
    elif request.method == "PUT":
        if song.user != request.user:
            return MUSIC_UNAUTHORIZED

        serializer = SongCreateSerializer(song, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            cache.delete(cache_key)
            serializer = SongWithoutUserSerializer(serializer.data)
            return CommonResponse('MUSIC_REQUEST_SONGS_UPDATED', status.HTTP_200_OK, serializer.data, "성공적으로 해당 신청곡을 수정했습니다.")
        return MUSIC_REQUEST_SONG_INVALID
    elif request.method == "DELETE":
        if not request.user.is_admin:
            if request.user != song.user:
                MUSIC_UNAUTHORIZED

        song.delete()
        cache.delete(cache_key)
        return CommonResponse('MUSIC_REQUEST_SONGS_DELETED', status.HTTP_204_NO_CONTENT, True, "성공적으로 해당 신청곡을 삭제했습니다.")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_history(request):
    cache_key = 'song_history'
    songs = cache.get(cache_key)

    if not songs:
        songs = Song.objects.filter(is_played=True) \
            .annotate(count_likes=Count('likes')) \
            .order_by('-id') \
            .select_related('user') \
            .prefetch_related('likes')

        cache.set(cache_key, songs, timeout=60 * 5)

    serializer = SongWithUserNicknameSerializer(songs, many=True)

    return CommonResponse('MUSIC_HISTORY_SONGS', status.HTTP_200_OK, serializer.data, '성공적으로 신청곡 기록을 불러왔습니다.')

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_history(request):
    songs = Song.objects.filter(user_id=request.user.pk, is_played=True) \
        .annotate(count_likes=Count('likes')) \
        .order_by('-id') \
        .select_related('user') \
        .prefetch_related('likes')
    serializer = SongWithUserNicknameSerializer(songs, many=True)

    return CommonResponse('MUSIC_HISTORY_SONGS_MY', status.HTTP_200_OK, serializer.data, '성공적으로 신청곡 기록을 불러왔습니다.')

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_history_song(request, song_id):
    song = Song.objects.filter(pk=song_id, is_played=True) \
        .annotate(count_likes=Count('likes')) \
        .order_by('-id') \
        .select_related('user') \
        .prefetch_related('likes')

    if not song:
        return MUSIC_HISTORY_SONG_NOTFOUND

    song = song.get()

    serializer = SongWithUserNicknameSerializer(song)
    return CommonResponse('MUSIC_HISTORY_SONGS_DETAIL', status.HTTP_200_OK, serializer.data, '성공적으로 해당 신청곡 기록을 불러왔습니다.')

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_create_comments(request, song_id):
    cache_key = 'comments_{}'.format(song_id)

    if request.method == "GET":
        comments = cache.get(cache_key)

        if not comments:
            comments = Comment.objects.filter(song_id=song_id).select_related('user')
            cache.set(cache_key, comments, timeout=60 * 5)

        serializer = CommentWithUsernameSerializer(comments, many=True)

        return CommonResponse('MUSIC_SONG_COMMENTS', status.HTTP_200_OK, serializer.data, '성공적으로 댓글을 불러왔습니다.')
    elif request.method == "POST":
        request.data['user'] = request.user.pk
        request.data['song'] = song_id

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            cache.delete(cache_key)
            return CommonResponse('MUSIC_SONG_COMMENTS_CREATED', status.HTTP_201_CREATED, serializer.data, '성공적으로 댓글을 달았습니다.')
        return MUSIC_SONG_COMMENTS_INVALID

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_put_delete_comment(request, song_id, comment_id):
    cache_key = 'comments_{}'.format(song_id)

    if request.method == "GET":
        comment = Comment.objects.filter(id=comment_id, song=song_id)

        if not comment:
            return MUSIC_SONG_COMMENTS_NOTFOUND

        comment = comment[0]

        serializer = CommentSerializer(comment)

        return CommonResponse('MUSIC_SONG_COMMENTS_DETAIL', status.HTTP_200_OK, serializer.data, '성공적으로 댓글을 불러왔습니다.')
    elif request.method == "PUT":
        request.data['user'] = request.user.pk
        request.data['song'] = song_id

        comment = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(comment, data=request.data)

        if comment.user != request.user:
            return MUSIC_UNAUTHORIZED

        if serializer.is_valid():
            serializer.save()
            cache.delete(cache_key)
            return CommonResponse('MUSIC_SONG_COMMENTS_UPDATED', status.HTTP_200_OK, serializer.data, '성공적으로 댓글을 수정했습니다.')
        return MUSIC_SONG_COMMENTS_INVALID
    elif request.method == "DELETE":
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return MUSIC_SONG_COMMENTS_NOTFOUND

        serializer = CommentSerializer(comment)

        if not request.user.is_admin:
            if request.user != comment.user:
                return MUSIC_UNAUTHORIZED

        comment.delete()
        cache.delete(cache_key)
        return CommonResponse('MUSIC_SONG_COMMENTS_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 댓글을 삭제했습니다.')

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_like(request, song_id):
    cache_key = 'songs'

    request.data['user'] = request.user.pk
    request.data['song'] = song_id

    serializer = LikeSerializer(data=request.data)

    if serializer.is_valid():
        song = Song.objects.get(pk=song_id)

        if song.user == request.user:
            return MUSIC_SONG_LIKE_SAME_USER

        like_history = Like.objects.filter(user=request.user, song__id=song_id)
        if not like_history:
            serializer.save()
            cache.delete(cache_key)
            return CommonResponse('MUSIC_SONG_LIKES_CREATED', status.HTTP_200_OK, True, '성공적으로 신청곡 좋아요를 눌렀습니다.')
        else:
            like_history.delete()
            cache.delete(cache_key)
            return CommonResponse('MUSIC_SONG_LIKES_DELETED', status.HTTP_200_OK, False, '성공적으로 신청곡 좋아요를 취소했습니다.')
    else:
        return MUSIC_SONG_LIKE_INVALID

@api_view(["POST"])
@permission_classes([IsAdminUser])
def song_play(request):
    songs = Song.objects.filter(is_played=False) \
        .annotate(count_likes=Count('likes')) \
        .order_by('-count_likes') \
        .select_related('user') \
        .prefetch_related('likes')

    if not songs:
        return MUSIC_PLAY_EMPTY

    original_song = songs[0]
    unplayed_songs = songs.values()[0]
    unplayed_songs['is_played'] = True

    serializer = SongPlaySerializer(original_song, data=unplayed_songs, partial=True)

    if serializer.is_valid():

        # TODO: 노래가 이미 실행 중이면, 실패 메시지를 보내야 함

        serializer.save()
        return CommonResponse('MUSIC_PLAY_SUCCESS', status.HTTP_200_OK, serializer.data, '성공적으로 노래를 재생했습니다.')
    return MUSIC_PLAY_INVALID

@api_view(["POST"])
@permission_classes([IsAdminUser])
def song_next(request):
    pass

@api_view(["POST"])
@permission_classes([IsAdminUser])
def song_prev(request):
    pass

@api_view(["POST"])
@permission_classes([IsAdminUser])
def song_clear(request):
    unplayed_songs = Song.objects.prefetch_related('user').filter(is_played=False)
    unplayed_songs.delete()

    return CommonResponse('MUSIC_SONG_CLEAR', status.HTTP_204_NO_CONTENT, True, '신청곡 목록을 모두 삭제했습니다.')