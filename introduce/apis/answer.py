import django_filters
from django.http import Http404
from rest_framework import authentication, viewsets, status
from rest_framework.permissions import IsAuthenticated

from moyeora_connector.exception_handler import CommonAPIException
from moyeora_connector.responses import CommonResponse

from ..models import (
    Answer,
)
from ..serializers import (
    AnswerSerializer,
    AnswerDetailSerializer
)

__all__ = (
    "AnswerViewSet",
)

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        if not self.request.user.is_admin:
            answers = Answer.objects.filter(user=self.request.user)\
                .select_related('user')\
                .prefetch_related('question')
        else:
            answers = Answer.objects.all()\
                .select_related('user')\
                .prefetch_related('question')

        return answers

    def get_object(self):
        try:
            object = super().get_object()
        except Http404:
            raise CommonAPIException('INTRO_ANSWER_NOT_FOUND', status.HTTP_200_OK, '해당 답변을 찾을 수 없습니다.')
        return object

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AnswerDetailSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs).data
        return CommonResponse('INTRO_ANSWER_LIST', status.HTTP_200_OK, response, '성공적으로 답변을 조회했습니다.')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, args, kwargs).data
        return CommonResponse('INTRO_ANSWER_DETAIL', status.HTTP_200_OK, response, '성공적으로 답변을 조회했습니다.')

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        response = super().create(request, args, kwargs).data
        return CommonResponse('INTRO_ANSWER_CREATED', status.HTTP_201_CREATED, response, '성공적으로 답변을 등록했습니다.')

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        response = serializer.validated_data
        return CommonResponse('INTRO_ANSWER_UPDATED', status.HTTP_200_OK, response, '성공적으로 답변이 수정됐습니다.')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, args, kwargs)
        return CommonResponse('INTRO_ANSWER_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 답변이 삭제됐습니다.')

