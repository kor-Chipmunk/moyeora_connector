from django.core.cache import cache
from django.http import Http404
from rest_framework import (
    authentication,
    viewsets,
    status, mixins
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from moyeora_connector.exception_handler import CommonAPIException
from moyeora_connector.responses import CommonResponse

from ..models import (
    Comment,
)
from ..serializers import (
    CommentSerializer,
    CommentCreationSerializer,
)

__all__ = (
    "CommentViewSet",
)

class CommentViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(song_id=self.kwargs['song_pk']) \
                    .select_related('user')

    def get_object(self):
        try:
            object = super().get_object()
        except Http404:
            raise CommonAPIException('MUSIC_SONG_NOT_FOUND', status.HTTP_200_OK, '해당 댓글을 찾을 수 없습니다.')
        return object

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreationSerializer
        return CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'song_id': self.kwargs['song_pk']
        })
        return context

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_COMMENTS', status.HTTP_200_OK, response, '성공적으로 댓글을 불러왔습니다.')

    def create(self, request, *args, **kwargs):
        response = super().create(request, args, kwargs).data
        return CommonResponse('MUSIC_SONG_COMMENTS_CREATED', status.HTTP_201_CREATED, response, '성공적으로 댓글을 등록했습니다.')

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = serializer.validated_data
        return CommonResponse('MUSIC_SONG_COMMENTS_UPDATED', status.HTTP_200_OK, response, '성공적으로 댓글을 수정됐습니다.')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, args, kwargs)
        return CommonResponse('MUSIC_SONG_COMMENTS_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 댓글을 삭제됐습니다.')
