from django.db import models

from user.models import User

class Song(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    is_played = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="신청곡을 넣은 유저")

    likes = models.ManyToManyField(User, through='Like', related_name="Like")

    class Meta:
        db_table = 'request_songs'

class Comment(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="댓글을 단 유저")
    song = models.ForeignKey(Song,
                             on_delete=models.CASCADE,
                             verbose_name="해당하는 신청곡")

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'song_comments'

class Like(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="좋아요를 누른 유저")
    song = models.ForeignKey(Song,
                             on_delete=models.CASCADE,
                             verbose_name="좋아요를 누른 신청곡")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'song_likes'
