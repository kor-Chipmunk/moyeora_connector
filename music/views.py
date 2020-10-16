# from datetime import timedelta
#
# from django.core.cache import cache
# from django.db.models import Count, F
# from django.utils import timezone
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
#
# from moyeora_connector.responses import CommonResponse
# from .serializers import *
# from .tasks import *
#
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def list_create_songs(request):
#     cache_key = 'songs'
#
#     if request.method == "GET":
#         songs = cache.get(cache_key)
#
#         if not songs:
#             songs = Song.objects.filter(is_played = False) \
#                 .order_by('-count_likes') \
#                 .select_related('user')
#             cache.set(cache_key, songs, timeout=60 * 5)
#
#         serializer = SongWithUserNicknameSerializer(songs, many=True)
#
#         return CommonResponse('MUSIC_REQUEST_SONGS', status.HTTP_200_OK, serializer.data, "신청곡 목록을 불러왔습니다.")
#     elif request.method == "POST":
#         request.data['user'] = request.user.pk
#
#         serializer = SongCreateSerializer(data=request.data)
#
#         if serializer.is_valid():
#             cache.delete(cache_key)
#             serializer.save()
#
#             serializer = SongWithoutUserSerializer(serializer.data)
#
#             return CommonResponse('MUSIC_REQUEST_SONGS_CREATED', status.HTTP_201_CREATED, serializer.data, "성공적으로 신청곡이 대기열에 올라갔습니다.")
#         print(serializer.errors)
#         return MUSIC_REQUEST_SONG_INVALID
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_my_songs(request):
#     songs = Song.objects.filter(user__id = request.user.pk) \
#         .order_by('-count_likes') \
#         .select_related('user')
#     serializer = SongWithUserNicknameSerializer(songs, many=True)
#
#     return CommonResponse('MUSIC_REQUEST_SONGS_MY', status.HTTP_200_OK, serializer.data, "성공적으로 신청곡을 불러왔습니다.")
#
# @api_view(["GET", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
# def retrieve_put_delete_song(request, song_id):
#     cache_key = 'songs'
#
#     try:
#         song = Song.objects.get(pk=song_id)
#     except Song.DoesNotExist:
#         return MUSIC_REQUEST_SONG_NOTFOUND
#
#     if request.method == "GET":
#         serializer = SongWithUserNicknameSerializer(song)
#         return CommonResponse('MUSIC_REQUEST_SONGS_DETAIL', status.HTTP_200_OK, serializer.data, "성공적으로 해당 신청곡을 불러왔습니다.")
#     elif request.method == "PUT":
#         if song.user != request.user:
#             return MUSIC_UNAUTHORIZED
#
#         serializer = SongCreateSerializer(song, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             cache.delete(cache_key)
#             serializer = SongWithoutUserSerializer(serializer.data)
#             return CommonResponse('MUSIC_REQUEST_SONGS_UPDATED', status.HTTP_200_OK, serializer.data, "성공적으로 해당 신청곡을 수정했습니다.")
#         return MUSIC_REQUEST_SONG_INVALID
#     elif request.method == "DELETE":
#         if not request.user.is_admin:
#             if request.user != song.user:
#                 MUSIC_UNAUTHORIZED
#
#         song.delete()
#         cache.delete(cache_key)
#         return CommonResponse('MUSIC_REQUEST_SONGS_DELETED', status.HTTP_204_NO_CONTENT, True, "성공적으로 해당 신청곡을 삭제했습니다.")
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_history(request):
#     cache_key = 'song_history'
#     songs = cache.get(cache_key)
#
#     if not songs:
#         songs = Song.objects.filter(is_played=True) \
#             .order_by('-id') \
#             .select_related('user')
#         cache.set(cache_key, songs, timeout=60 * 5)
#
#     serializer = SongWithUserNicknameSerializer(songs, many=True)
#
#     return CommonResponse('MUSIC_HISTORY_SONGS', status.HTTP_200_OK, serializer.data, '성공적으로 신청곡 기록을 불러왔습니다.')
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_my_history(request):
#     songs = Song.objects.filter(user_id=request.user.pk, is_played=True) \
#         .order_by('-id') \
#         .select_related('user')
#     serializer = SongWithUserNicknameSerializer(songs, many=True)
#
#     return CommonResponse('MUSIC_HISTORY_SONGS_MY', status.HTTP_200_OK, serializer.data, '성공적으로 신청곡 기록을 불러왔습니다.')
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_history_song(request, song_id):
#     song = Song.objects.filter(pk=song_id, is_played=True) \
#         .select_related('user') \
#
#     if not song:
#         return MUSIC_HISTORY_SONG_NOTFOUND
#
#     song = song.get()
#
#     serializer = SongWithUserNicknameSerializer(song)
#     return CommonResponse('MUSIC_HISTORY_SONGS_DETAIL', status.HTTP_200_OK, serializer.data, '성공적으로 해당 신청곡 기록을 불러왔습니다.')
#
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def list_create_comments(request, song_id):
#     cache_key = 'comments_{}'.format(song_id)
#
#     if request.method == "GET":
#         comments = cache.get(cache_key)
#
#         if not comments:
#             comments = Comment.objects.filter(song_id=song_id).select_related('user')
#             cache.set(cache_key, comments, timeout=60 * 5)
#
#         serializer = CommentWithUsernameSerializer(comments, many=True)
#
#         return CommonResponse('MUSIC_SONG_COMMENTS', status.HTTP_200_OK, serializer.data, '성공적으로 댓글을 불러왔습니다.')
#     elif request.method == "POST":
#         request.data['user'] = request.user.pk
#         request.data['song'] = song_id
#
#         serializer = CommentSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             cache.delete(cache_key)
#             return CommonResponse('MUSIC_SONG_COMMENTS_CREATED', status.HTTP_201_CREATED, serializer.data, '성공적으로 댓글을 달았습니다.')
#         return MUSIC_SONG_COMMENTS_INVALID
#
# @api_view(["GET", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
# def retrieve_put_delete_comment(request, song_id, comment_id):
#     cache_key = 'comments_{}'.format(song_id)
#
#     if request.method == "GET":
#         comment = Comment.objects.filter(id=comment_id, song=song_id)
#
#         if not comment:
#             return MUSIC_SONG_COMMENTS_NOTFOUND
#
#         comment = comment[0]
#
#         serializer = CommentSerializer(comment)
#
#         return CommonResponse('MUSIC_SONG_COMMENTS_DETAIL', status.HTTP_200_OK, serializer.data, '성공적으로 댓글을 불러왔습니다.')
#     elif request.method == "PUT":
#         request.data['user'] = request.user.pk
#         request.data['song'] = song_id
#
#         comment = Comment.objects.get(id=comment_id)
#         serializer = CommentSerializer(comment, data=request.data)
#
#         if comment.user != request.user:
#             return MUSIC_UNAUTHORIZED
#
#         if serializer.is_valid():
#             serializer.save()
#             cache.delete(cache_key)
#             return CommonResponse('MUSIC_SONG_COMMENTS_UPDATED', status.HTTP_200_OK, serializer.data, '성공적으로 댓글을 수정했습니다.')
#         return MUSIC_SONG_COMMENTS_INVALID
#     elif request.method == "DELETE":
#         try:
#             comment = Comment.objects.get(pk=comment_id)
#         except Comment.DoesNotExist:
#             return MUSIC_SONG_COMMENTS_NOTFOUND
#
#         serializer = CommentSerializer(comment)
#
#         if not request.user.is_admin:
#             if request.user != comment.user:
#                 return MUSIC_UNAUTHORIZED
#
#         comment.delete()
#         cache.delete(cache_key)
#         return CommonResponse('MUSIC_SONG_COMMENTS_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 댓글을 삭제했습니다.')
#
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def post_like(request, song_id):
#     cache_key = 'songs'
#
#     serializer = LikeSerializer(data=request.data, context={'request': request, 'song_id': song_id})
#
#     try:
#         serializer.is_valid(raise_exception=True)
#     except ValueError:
#         return MUSIC_SONG_LIKE_SAME_USER
#
#     result = serializer.save()
#     cache.delete(cache_key)
#
#     if result:
#         return CommonResponse('MUSIC_SONG_LIKES_CREATED', status.HTTP_200_OK, True, '성공적으로 신청곡 좋아요를 눌렀습니다.')
#     else:
#         return CommonResponse('MUSIC_SONG_LIKES_DELETED', status.HTTP_200_OK, False, '성공적으로 신청곡 좋아요를 취소했습니다.')
#
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def comment_like(request, song_id, comment_id):
#     serializer = CommentLikeSerializer(data=request.data, context={'request': request, 'comment_id': comment_id})
#
#     try:
#         serializer.is_valid(raise_exception=True)
#     except ValueError:
#         return MUSIC_SONG_COMMENTS_LIKE_SAME_USER
#
#     result = serializer.save()
#
#     if result:
#         return CommonResponse('MUSIC_SONG_COMMENTS_LIKES_CREATED', status.HTTP_200_OK, True, '성공적으로 댓글 좋아요를 눌렀습니다.')
#     else:
#         return CommonResponse('MUSIC_SONG_COMMENTS_LIKES_DELETED', status.HTTP_200_OK, False, '성공적으로 댓글 좋아요를 취소했습니다.')
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_weekly_song(request):
#     now = timezone.localtime()
#     week_start = (now - timedelta(days = now.weekday())).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
#     week_end = (now + timedelta(days=7 - now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
#
#     songs = Song.objects.filter(is_played = True) \
#         .filter(created_at__range=(week_start, week_end)) \
#         .values('title', 'url', 'count_likes', 'count_comments') \
#         .annotate(count=Count('url')) \
#         .order_by('-count')
#
#     return CommonResponse('MUSIC_SONG_WEEKLY_LIST', status.HTTP_200_OK, songs, '성공적으로 금주 신청곡 통계를 조회했습니다.')
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_monthly_song(request):
#     now = timezone.localtime()
#
#     month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     month_end = now.replace(day=28, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=4)
#     month_end -= timedelta(days=month_end.day)
#
#     songs = Song.objects.filter(is_played=True) \
#         .filter(created_at__range=(month_start, month_end)) \
#         .values('title', 'count_likes', 'count_comments', 'url') \
#         .annotate(count=Count('url')) \
#         .order_by('-count')
#
#     return CommonResponse('MUSIC_SONG_MONTHLY_LIST', status.HTTP_200_OK, songs, '성공적으로 금달 신청곡 통계를 조회했습니다.')
#
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_yearly_song(request):
#     now = timezone.localtime()
#
#     year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
#     year_end = year_start.replace(year=year_start.year+1)
#
#     songs = Song.objects.filter(is_played=True) \
#         .filter(created_at__range=(year_start, year_end)) \
#         .values('title', 'count_likes', 'count_comments', 'url') \
#         .annotate(count=Count('url')) \
#         .order_by('-count')
#
#     return CommonResponse('MUSIC_SONG_MONTHLY_LIST', status.HTTP_200_OK, songs, '성공적으로 금년 신청곡 통계를 조회했습니다.')
#
# @api_view(["POST"])
# @permission_classes([IsAdminUser])
# def song_play(request):
#     songs = Song.objects.filter(is_played=False) \
#         .order_by('-count_likes') \
#         .select_related('user')
#
#     if not songs:
#         return MUSIC_PLAY_EMPTY
#
#     original_song = songs[0]
#     unplayed_songs = songs.values()[0]
#     unplayed_songs['is_played'] = True
#
#     serializer = SongPlaySerializer(original_song, data=unplayed_songs)
#
#     if serializer.is_valid():
#         song_url = play_song(unplayed_songs['id'], serializer.validated_data['title'], serializer.validated_data['url'])
#         serializer.validated_data['url'] = song_url
#
#         serializer.save()
#         return CommonResponse('MUSIC_PLAY_SUCCESS', status.HTTP_200_OK, serializer.data, '성공적으로 노래를 재생했습니다.')
#     return MUSIC_PLAY_INVALID
#
# @api_view(["POST"])
# @permission_classes([IsAdminUser])
# def song_clear(request):
#     unplayed_songs = Song.objects.prefetch_related('user').filter(is_played=False)
#     unplayed_songs.delete()
#
#     return CommonResponse('MUSIC_SONG_CLEAR', status.HTTP_204_NO_CONTENT, True, '신청곡 목록을 모두 삭제했습니다.')