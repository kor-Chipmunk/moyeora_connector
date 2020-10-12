from rest_framework import status

from moyeora_connector.responses import ErrorResponse

INTRO_UNAUTHORIZE_ADMIN = ErrorResponse(
    code='INTRO_UNAUTHORIZE_ADMIN',
    status=status.HTTP_401_UNAUTHORIZED,
    message='관리자만 접근 가능합니다.'
)

INTRO_QUESTION_INVALID = ErrorResponse(
    code='INTRO_QUESTION_INVALID',
    status=status.HTTP_400_BAD_REQUEST,
    message='질문 생성 양식이 일치하지 않습니다.'
)

INTRO_QUESTION_NOTFOUND = ErrorResponse(
    code='INTRO_QUESTION_NOTFOUND',
    status=status.HTTP_200_OK,
    message='해당 질문을 찾지 못했습니다.'
)

INTRO_ANSWER_INVALID = ErrorResponse(
    code='INTRO_ANSWER_INVALID',
    status=status.HTTP_400_BAD_REQUEST,
    message='답변 작성 양식이 일치하지 않습니다.'
)

INTRO_ANSWER_NOTFOUND = ErrorResponse(
    code='INTRO_ANSWER_NOTFOUND',
    status=status.HTTP_200_OK,
    message='해당 답변을 찾지 못했습니다.'
)

INTRO_ANSWER_UNAUTHORIZE = ErrorResponse(
    code='INTRO_ANSWER_UNAUTHORIZE',
    status=status.HTTP_401_UNAUTHORIZED,
    message='해당 답변의 작성자만 접근할 수 있습니다.'
)