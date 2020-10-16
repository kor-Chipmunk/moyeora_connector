from django.http import Http404
from rest_framework import authentication, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from moyeora_connector.common.utils.paginations import StandardResultsSetPagination
from moyeora_connector.exception_handler import CommonAPIException
from moyeora_connector.responses import CommonResponse

from ..models import (
    Song,
)
from ..serializers import (
    SongSerializer,
    SongWithUsernameSerializer,
)

__all__ = (
    "RequestSongViewSet",
    "HistorySongViewSet",
)

class RequestSongViewSet(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'url']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.action == "list_my":
            return self.queryset.filter(is_played=False, user_id=self.request.user.pk) \
                    .order_by('-count_likes') \
                    .select_related('user')

        return self.queryset.filter(is_played=False) \
                    .order_by('-count_likes') \
                    .select_related('user')

    def get_object(self):
        try:
            object = super().get_object()
        except Http404:
            raise CommonAPIException('MUSIC_SONG_NOT_FOUND', status.HTTP_200_OK, '해당 신청곡을 찾을 수 없습니다.')
        return object

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "list_my"]:
            return SongWithUsernameSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_LIST', status.HTTP_200_OK, response, '성공적으로 신청곡을 조회했습니다.')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_DETAIL', status.HTTP_200_OK, response, '성공적으로 신청곡을 조회했습니다.')

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        response = super().create(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_CREATED', status.HTTP_201_CREATED, response, '성공적으로 신청곡을 등록했습니다.')

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        response = serializer.validated_data
        return CommonResponse('MUSIC_SONG_UPDATED', status.HTTP_200_OK, response, '성공적으로 신청곡을 수정됐습니다.')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, args, kwargs)
        return CommonResponse('MUSIC_SONG_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 신청곡을 삭제됐습니다.')

    @action(methods=['get'], detail=False, url_name='my', url_path='my')
    def list_my(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_MY', status.HTTP_200_OK, response, '성공적으로 신청곡을 조회했습니다.')

class HistorySongViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SongWithUsernameSerializer
    queryset = Song.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'url']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.action == "list_my":
            return self.queryset.filter(is_played=True, user__id=self.request.user.pk) \
                        .select_related('user')

        return self.queryset.filter(is_played=True) \
            .select_related('user')

    def get_object(self):
        try:
            object = super().get_object()
        except Http404:
            raise CommonAPIException('MUSIC_SONG_NOT_FOUND', status.HTTP_200_OK, '해당 신청곡을 찾을 수 없습니다.')
        return object

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_HISTORY', status.HTTP_200_OK, response, '성공적으로 신청곡을 조회했습니다.')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_HISTORY_DETAIL', status.HTTP_200_OK, response, '성공적으로 신청곡을 조회했습니다.')

    @action(methods=['get'], detail=False, url_name='my', url_path='my')
    def list_my(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_MY', status.HTTP_200_OK, response, '성공적으로 신청곡을 조회했습니다.')