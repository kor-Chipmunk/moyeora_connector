from django.db import models

from user.models import User

class Song(models.Model):
    title = models.CharField(verbose_name="노래 키워드", max_length=255)
    url = models.CharField(verbose_name="동영상 주소", max_length=255, blank=True, null=True, default='')
    is_played = models.BooleanField(verbose_name="재생 이력 여부", default=False)
    created_at = models.DateTimeField(verbose_name="생성 일자", auto_now_add=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="신청곡을 넣은 유저"
    )

    count_likes = models.PositiveIntegerField(verbose_name="신청곡 좋아요 개수", default=0)
    count_comments = models.PositiveIntegerField(verbose_name="댓글 개수", default=0)

    likes = models.ManyToManyField(
        User,
        through='Like',
        through_fields=('song', 'user'),
        related_name='song_likes',
        verbose_name="신청곡 좋아요",
    )

    class Meta:
        db_table = 'request_songs'
        verbose_name = '신청곡'
        verbose_name_plural = f"{verbose_name} 목록"

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="댓글을 단 유저"
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        verbose_name="해당하는 신청곡"
    )

    content = models.TextField(verbose_name="댓글 내용")
    created_at = models.DateTimeField(verbose_name="생성 일자", auto_now_add=True)

    count_likes = models.PositiveIntegerField(verbose_name="좋아요 개수", default=0)

    likes = models.ManyToManyField(
        User,
        through='CommentLike',
        through_fields=('comment', 'user'),
        related_name='comment_likes',
        verbose_name='댓글 좋아요',
    )

    class Meta:
        db_table = 'song_comments'
        verbose_name = '신청곡 댓글'
        verbose_name_plural = f"{verbose_name} 목록"

class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="좋아요를 누른 유저"
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        verbose_name="좋아요를 누른 신청곡"
    )

    created_at = models.DateTimeField(verbose_name="생성 일자", auto_now_add=True)

    class Meta:
        db_table = 'song_likes'
        verbose_name = '신청곡 좋아요'
        verbose_name_plural = f"{verbose_name} 목록"

class CommentLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="댓글 좋아요를 누른 유저"
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name="좋아요를 누른 댓글"
    )

    created_at = models.DateTimeField(verbose_name="생성 일자", auto_now_add=True)

    class Meta:
        db_table = 'comment_likes'
        verbose_name = '댓글 좋아요'
        verbose_name_plural = f"{verbose_name} 목록"