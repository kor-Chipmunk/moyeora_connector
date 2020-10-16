from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.exceptions import PermissionDenied, APIException, NotAuthenticated
from rest_framework.response import Response

class CommonAPIException(exceptions.APIException):
    code = ''
    status = 0
    message = ''
    detail = {}

    def __init__(self, code, status, message, detail={}):
        self.code = code
        self.status = status
        self.message = message
        self.detail = detail

def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = CommonAPIException(
            'NOT_FOUND',
            status.HTTP_404_NOT_FOUND,
            '페이지를 찾을 수 없습니다.'
        )
    elif isinstance(exc, PermissionDenied):
        exc = CommonAPIException(
            'PERMISSION_DENIED',
            status.HTTP_401_UNAUTHORIZED,
            '접근 권한이 없습니다.'
        )
    elif isinstance(exc, NotAuthenticated):
        exc = CommonAPIException(
            'UNAUTHENTICATED',
            status.HTTP_401_UNAUTHORIZED,
            '접근 권한이 없습니다.'
        )

    headers = None

    if isinstance(exc, APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

    if not isinstance(exc, CommonAPIException) and isinstance(exc, APIException):
        exc = CommonAPIException(
            'UNHANDLED_EXCEPTION',
            exc.status_code,
            '',
            exc.detail
        )

    if isinstance(exc, CommonAPIException):
        return Response(
            exc.__dict__,
            status=exc.status,
            headers=headers
        )

    return None