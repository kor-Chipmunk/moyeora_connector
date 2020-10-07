from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerCreationSerializer, AnswerDetailSerializer, \
    AnswerOnlyContentSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_list_questions(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not request.user.is_admin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_update_destory_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = QuestionSerializer(question)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if not request.user.is_admin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = QuestionSerializer(question, data=request.data, partial=True)

        if serializer.is_valid():
            if request.user != serializer.validated_data['user']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if not request.user.is_admin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_create_answers(request):
    if request.method == "GET":
        if not request.user.is_admin:
            answers = Answer.objects.filter(user=request.user)\
                .select_related('user')\
                .prefetch_related('question')
        else:
            answers = Answer.objects.all()\
                .select_related('user')\
                .prefetch_related('question')

        serializer = AnswerDetailSerializer(answers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        request.data['user'] = request.user.pk
        serializer = AnswerCreationSerializer(data=request.data)

        if serializer.is_valid():
            if request.user != serializer.validated_data['user']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer.save()

            serializer = AnswerOnlyContentSerializer(serializer.data)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_update_destory_answer(request, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_admin:
        if request.user != answer.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = AnswerDetailSerializer(answer)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        request.data['user'] = request.user.pk

        serializer = AnswerCreationSerializer(answer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)