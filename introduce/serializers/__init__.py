from rest_framework import serializers

from user.serializers import UserNicknameSerializer

from ..models import (
    Question,
    Answer,
)

QUESTION_FIELDS = (
    "id",
    "content",
    "created_at",
)

ANSWER_FIELDS = (
    "id",
    "content",
    "created_at",
    "user",
    "question",
)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = QUESTION_FIELDS

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ANSWER_FIELDS

class AnswerDetailSerializer(serializers.ModelSerializer):
    user = UserNicknameSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ANSWER_FIELDS