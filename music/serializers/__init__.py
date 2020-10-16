from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from user.serializers import UserNicknameSerializer

from ..models import (
    Song,
    Comment,
    Like,
    CommentLike,
)

SONG_FIELDS = (
    "id",
    "title",
    "url",
    "is_played",
    "created_at",
    "user",
    "count_likes",
    "count_comments",
)

COMMENT_FIELDS = (
    "id",
    "user",
    "song",
    "content",
    "created_at",
    "count_likes",
)

LIKE_FIELDS = (
    "id",
    "user",
    "song",
    "created_at",
)

COMMENT_LIKE_FIELDS = (
    "id",
    "user",
    "comment",
    "created_at",
)

SONG_STAT_FIELDS = (
    'title',
    'url',
    'count_likes',
    'count_comments',
)

class SongSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    url = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = Song
        fields = SONG_FIELDS

class SongWithUsernameSerializer(serializers.ModelSerializer):
    user = UserNicknameSerializer(read_only=True)

    class Meta:
        model = Song
        fields = SONG_FIELDS

class SongStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = SONG_STAT_FIELDS

class CommentSerializer(serializers.ModelSerializer):
    user = UserNicknameSerializer(read_only=True)
    song = serializers.HiddenField(default=-1)

    class Meta:
        model = Comment
        fields = COMMENT_FIELDS

class CommentCreationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    song = serializers.HiddenField(default=-1)

    def validate(self, data):
        song_object = get_object_or_404(Song, pk=self.context['song_id'])
        data['song'] = song_object
        return data

    def save(self):
        song = self.validated_data['song']
        comment, comment_created = Comment.objects.get_or_create(self.validated_data)

        if comment_created:
            song.count_comments += 1
            song.save()

        return comment

    class Meta:
        model = Comment
        fields = COMMENT_FIELDS


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    song = serializers.HiddenField(default=-1)

    def validate(self, data):
        data['song'] = get_object_or_404(Song, pk=self.context['song_id'])

        if data['song'].user_id == data['user'].pk:
            raise ValueError('같은 유저 발생!')

        return data

    def save(self):
        song = self.validated_data['song']
        user = self.validated_data['user']
        like, like_created = Like.objects.get_or_create(song=song, user=user)

        if like_created:
            song.count_likes += 1
        else:
            like.delete()
            song.count_likes -= 1

        song.save()

        return like_created

    class Meta:
        model = Like
        fields = '__all__'

class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comment = serializers.HiddenField(default=-1)

    def validate(self, data):
        data['comment'] = get_object_or_404(Comment, pk=self.context['comment_id'])

        if data['comment'].user_id == data['user'].pk:
            raise ValueError('같은 유저 발생!')

        return data

    def save(self):
        comment = self.validated_data['comment']
        user = self.validated_data['user']
        like, like_created = CommentLike.objects.get_or_create(comment=comment, user=user)

        if like_created:
            comment.count_likes += 1
        else:
            like.delete()
            comment.count_likes -= 1

        comment.save()

        return like_created

    class Meta:
        model = CommentLike
        fields = '__all__'