from django.db import models

from user.models import User


class Question(models.Model):
    content = models.TextField(verbose_name="질문 내용")
    created_at = models.DateTimeField(verbose_name="생성 일자", auto_now_add=True)

    class Meta:
        verbose_name = "질문"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = ("-id", )
        db_table = 'intro_questions'

    def __str__(self):
        return self.content

class Answer(models.Model):
    content = models.TextField(verbose_name="답변 내용")
    created_at = models.DateTimeField(verbose_name="생성 일자", auto_now_add=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="답변을 한 유저"
    )

    question = models.ForeignKey(
        Question,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="답변한 질문"
    )

    class Meta:
        verbose_name = "답변"
        verbose_name_plural = f"{verbose_name} 목록"
        db_table = 'intro_answers'
        unique_together = ('user', 'question')

    def __str__(self):
        return self.content