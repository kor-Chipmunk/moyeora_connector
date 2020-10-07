from rest_framework import serializers

from user.serializers import UserNicknameSerializer
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class QuestionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'content', )

class AnswerCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AnswerOnlyContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('user', 'question', )

class AnswerDetailSerializer(serializers.ModelSerializer):
    user = UserNicknameSerializer(read_only=True)
    question = QuestionTitleSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'