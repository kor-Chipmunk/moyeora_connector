from rest_framework import (
    authentication,
    status,
    mixins,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from moyeora_connector.responses import CommonResponse

from ..models import (
    Comment,
    Like,
)
from ..serializers import (
    LikeSerializer,
    CommentLikeSerializer,
)

__all__ = (
    "SongLikeViewSet",
    "CommentLikeViewSet",
)

class SongLikeViewSet(GenericViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'song_id': self.kwargs['song_pk']
        })
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        headers = self.get_success_headers(serializer.data)

        if result:
            return CommonResponse('MUSIC_SONG_LIKES_CREATED', status.HTTP_200_OK, True, '성공적으로 신청곡 좋아요를 눌렀습니다.', headers=headers)
        else:
            return CommonResponse('MUSIC_SONG_LIKES_DELETED', status.HTTP_200_OK, False, '성공적으로 신청곡 좋아요를 취소했습니다.', headers=headers)

class CommentLikeViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CommentLikeSerializer
    queryset = Comment.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'song_id': self.kwargs['song_pk'],
            'comment_id': self.kwargs['comment_pk'],
        })
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        headers = self.get_success_headers(serializer.data)

        if result:
            return CommonResponse('MUSIC_SONG_COMMENTS_LIKES_CREATED', status.HTTP_200_OK, True, '성공적으로 댓글 좋아요를 눌렀습니다.', headers=headers)
        else:
            return CommonResponse('MUSIC_SONG_COMMENTS_LIKES_DELETED', status.HTTP_200_OK, False, '성공적으로 댓글 좋아요를 취소했습니다.', headers=headers)