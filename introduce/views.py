from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from moyeora_connector.responses import CommonResponse
from .exceptions import *
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerCreationSerializer, AnswerDetailSerializer, \
    AnswerOnlyContentSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_list_questions(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)

        return CommonResponse('INTRODUCE_QUESTION_LIST', status.HTTP_200_OK, serializer.data, '성공적으로 질문을 조회했습니다.')
    elif request.method == "POST":
        if not request.user.is_admin:
            return INTRO_UNAUTHORIZE_ADMIN

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return CommonResponse('INTRODUCE_QUESTION_CREATED', status.HTTP_201_CREATED, serializer.data, '성공적으로 질문을 등록했습니다.')
        return INTRO_QUESTION_INVALID

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_update_destory_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return INTRO_QUESTION_NOTFOUND

    if request.method == "GET":
        serializer = QuestionSerializer(question)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if not request.user.is_admin:
            return INTRO_UNAUTHORIZE_ADMIN

        serializer = QuestionSerializer(question, data=request.data, partial=True)

        if serializer.is_valid():
            if request.user != serializer.validated_data['user']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer.save()

            return CommonResponse('INTRO_QUESTION_UPDATED', status.HTTP_201_CREATED, serializer.data, '성공적으로 질문이 수정됐습니다.')
        return INTRO_QUESTION_INVALID
    elif request.method == "DELETE":
        if not request.user.is_admin:
            return INTRO_UNAUTHORIZE_ADMIN

        question.delete()
        return CommonResponse('INTRO_QUESTION_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 질문이 삭제됐습니다.')

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

        return CommonResponse('INTRO_ANSWER_LIST', status.HTTP_200_OK, serializer.data, '성공적으로 답변 목록을 조회했습니다.')
    elif request.method == "POST":
        request.data['user'] = request.user.pk
        serializer = AnswerCreationSerializer(data=request.data)

        if serializer.is_valid():
            if request.user != serializer.validated_data['user']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer.save()

            serializer = AnswerOnlyContentSerializer(serializer.data)

            return CommonResponse('INTRO_ANSWER_CREATED', status.HTTP_201_CREATED, serializer.data, '성공적으로 답변이 작성됐습니다.')
        return INTRO_ANSWER_INVALID

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def retrieve_update_destory_answer(request, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        return INTRO_ANSWER_NOTFOUND

    if not request.user.is_admin:
        if request.user != answer.user:
            return INTRO_ANSWER_UNAUTHORIZE

    if request.method == "GET":
        serializer = AnswerDetailSerializer(answer)

        return CommonResponse('INTRO_ANSWER_LIST', status.HTTP_200_OK, serializer.data, '성공적으로 답변 목록을 작성했습니다.')
    elif request.method == "PUT":
        request.data['user'] = request.user.pk

        serializer = AnswerCreationSerializer(answer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return CommonResponse('INTRO_ANSWER_CREATED', status.HTTP_201_CREATED, serializer.data, '성공적으로 답변을 작성했습니다.')
        return INTRO_ANSWER_INVALID
    elif request.method == "DELETE":
        answer.delete()
        return CommonResponse('INTRO_ANSWER_DELETED', status.HTTP_204_NO_CONTENT, True, '성공적으로 답변을 삭제했습니다.')