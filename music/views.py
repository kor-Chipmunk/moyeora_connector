from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Song, Comment, Like
from .serializers import SongCreateSerializer, SongWithUserNicknameSerializer, CommentSerializer, LikeSerializer, \
    SongWithoutUserSerializer, CommentWithUsernameSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_create_songs(request):
    if request.method == "GET":
        songs = Song.objects.annotate(count_likes=Count('likes')) \
            .order_by('-count_likes')\
            .select_related('user')\
            .prefetch_related('likes')

        serializer = SongWithUserNicknameSerializer(songs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        request.data['user'] = request.user.pk

        serializer = SongCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            serializer = SongWithoutUserSerializer(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_songs(request):
    songs = Song.objects.filter(user__id = request.user.pk)\
        .annotate(count_likes=Count('likes'))\
        .order_by('-count_likes')\
        .select_related('user')
    serializer = SongWithUserNicknameSerializer(songs, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_put_delete_song(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SongWithUserNicknameSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if song.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = SongCreateSerializer(song, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            serializer = SongWithoutUserSerializer(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if not request.user.is_admin:
            if request.user != song.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_history(request):
    songs = Song.objects.filter(is_played=True).order_by('-id').select_related('user')
    serializer = SongWithUserNicknameSerializer(songs, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_history(request):
    songs = Song.objects.filter(user_id=request.user.pk, is_played=True).order_by('-id').select_related('user')
    serializer = SongWithUserNicknameSerializer(songs, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_history_song(request, song_id):
    song = Song.objects.filter(pk=song_id, is_played=True).select_related('user')
    serializer = SongWithUserNicknameSerializer(song)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_create_comments(request, song_id):
    if request.method == "GET":
        comments = Comment.objects.filter(song_id=song_id).select_related('user')
        serializer = CommentWithUsernameSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        request.data['user'] = request.user.pk
        request.data['song'] = song_id

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_put_delete_comment(request, song_id, comment_id):
    if request.method == "GET":
        comment = Comment.objects.filter(id=comment_id, song=song_id)
        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        request.data['user'] = request.user.pk
        request.data['song'] = song_id

        comment = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(comment, data=request.data)

        if comment.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comment)

        if not request.user.is_admin:
            if request.user != comment.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_like(request, song_id):
    request.data['user'] = request.user.pk
    request.data['song'] = song_id

    serializer = LikeSerializer(data=request.data)

    if serializer.is_valid():
        song = Song.objects.get(pk=song_id)
        # if song.user == request.user:
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        like_history = Like.objects.filter(user=request.user, song__id=song_id)
        if not like_history:
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def song_play(request):
    popped_song = Song.objects.all()[0]

    serializer = SongCreateSerializer(data=popped_song)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_204_NO_CONTENT)

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
    unplayed_songs = Song.objects.all().prefetch_related('user')
    unplayed_songs.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)