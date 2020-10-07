from rest_framework import serializers

from user.serializers import UserLoginSerializer, UserNicknameSerializer
from .models import Song, Comment, Like


class SongCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SongWithoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'url', 'created_at', )

class SongWithUserNicknameSerializer(serializers.ModelSerializer):
    user = UserNicknameSerializer(read_only=True)
    count_likes = serializers.IntegerField()

    class Meta:
        model = Song
        exclude = ('is_played', 'likes')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentWithUsernameSerializer(serializers.ModelSerializer):
    user = UserNicknameSerializer(read_only=True)
    song = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'