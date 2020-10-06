from django.db import models

from user.models import User


class Question(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'intro_questions'

class Answer(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="답변을 한 유저")

    question = models.ForeignKey(Question,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name="답변한 질문")

    class Meta:
        db_table = 'intro_answers'
        unique_together = ('user', 'question')