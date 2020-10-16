from datetime import timedelta

from django.core.cache import cache
from django.db.models import Count, Sum, F, OuterRef, Subquery
from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend, filters
from requests import Response
from rest_framework import (
    authentication,
    viewsets,
    status, mixins, generics
)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from moyeora_connector.common.utils.paginations import StandardResultsSetPagination
from moyeora_connector.exception_handler import CommonAPIException
from moyeora_connector.responses import CommonResponse

from ..models import (
    Song
)
from ..serializers import (
    SongSerializer,
    SongWithUsernameSerializer, SongStatsSerializer,
)

__all__ = (
    "SongStatisticsViewSet",
)

class SongStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = SongStatsSerializer
    queryset = Song.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'id': ['exact'],
        'url': ['exact'],
        'title': ['exact'],
        'created_at': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }
    search_fields = ['title', 'url']
    ordering_fields = '__all__'

    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(is_played = True)

    @action(methods=["GET"], detail=False, url_path="weekly", url_name="weekly")
    def weekly(self, request, *args, **kwargs):
        now = timezone.localtime()
        week_start = (now - timedelta(days = now.weekday())).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        week_end = (now + timedelta(days = 7 - now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

        # latest_song_per_url = self.get_queryset().filter(url=OuterRef('url')).order_by('-id')[0]

        filtered_queryset = self.get_queryset() \
            .filter(created_at__range=(week_start, week_end))

        songs = self.get_queryset() \
            .filter(created_at__range=(week_start, week_end)) \
            .values('url') \
            .annotate(count_viewed=Count('url')) \
            .order_by('-count_viewed')

        return CommonResponse('MUSIC_SONG_WEEKLY_LIST', status.HTTP_200_OK, songs, '성공적으로 금주 신청곡 통계를 조회했습니다.')

    @action(methods=["GET"], detail=False, url_path="monthly", url_name="monthly")
    def monthly(self, request, *args, **kwargs):
        now = timezone.localtime()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = now.replace(day=28, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=4)
        month_end -= timedelta(days=month_end.day)

        songs = self.get_queryset() \
            .filter(created_at__range=(month_start, month_end)) \
            .values('url') \
            .annotate(count_viewed=Count('url')) \
            .order_by('-count_viewed')

        return CommonResponse('MUSIC_SONG_MONTHLY_LIST', status.HTTP_200_OK, songs, '성공적으로 금달 신청곡 통계를 조회했습니다.')

    @action(methods=["GET"], detail=False, url_path="yearly", url_name="yearly")
    def yearly(self, request, *args, **kwargs):
        now = timezone.localtime()
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        year_end = year_start.replace(year=year_start.year+1)

        songs = self.get_queryset() \
            .filter(created_at__range=(year_start, year_end)) \
            .values('url') \
            .annotate(count_viewed=Count('url')) \
            .order_by('-count_viewed')

        return CommonResponse('MUSIC_SONG_MONTHLY_LIST', status.HTTP_200_OK, songs, '성공적으로 금년 신청곡 통계를 조회했습니다.')