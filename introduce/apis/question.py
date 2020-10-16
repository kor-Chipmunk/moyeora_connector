import django_filters
from django.core.cache import cache
from django.http import Http404
from rest_framework import authentication, viewsets, status

from moyeora_connector.common.utils.permissions import IsAdminOrReadOnly
from moyeora_connector.exception_handler import CommonAPIException
from moyeora_connector.responses import CommonResponse

from ..models import (
    Question,
)
from ..serializers import (
    QuestionSerializer,
)

__all__ = (
    "QuestionViewSet",
)

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    cache_key = "intro_questions"

    def get_object(self):
        try:
            object = super().get_object()
        except Http404:
            raise CommonAPIException('INTRO_QUESTION_NOT_FOUND', status.HTTP_200_OK, '해당 질문을 찾을 수 없습니다.')

    def list(self, request, *args, **kwargs):
        response = cache.get(self.cache_key)
        if not response:
            response = super().list(request, args, kwargs).data
            cache.set(self.cache_key, response, timeout=60 * 60 * 24)
        return CommonResponse('INTRO_QUESTION_LIST', status.HTTP_200_OK, response, '성공적으로 질문을 조회했습니다.')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, args, kwargs).data
        return CommonResponse('INTRO_QUESTION_DETAIL', status.HTTP_200_OK, response, '성공적으로 질문을 조회했습니다.')

    def create(self, request, *args, **kwargs):
        response = super().create(request, args, kwargs).data
        cache.delete(self.cache_key)
        return CommonResponse('INTRO_QUESTION_CREATED', status.HTTP_201_CREATED, response, '성공적으로 질문을 등록했습니다.')

    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs).data
        cache.delete(self.cache_key)
        return CommonResponse('INTRO_QUESTION_UPDATED', status.HTTP_200_OK, response, '성공적으로 질문이 수정됐습니다.')

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, args, kwargs).data
        cache.delete(self.cache_key)
        return CommonResponse('INTRO_QUESTION_UPDATED', status.HTTP_200_OK, response, '성공적으로 질문이 수정됐습니다.')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, args, kwargs)
        cache.delete(self.cache_key)
        return CommonResponse('INTRO_QUESTION_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 질문이 삭제됐습니다.')