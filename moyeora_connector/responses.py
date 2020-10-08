from rest_framework.response import Response


class CommonResponse(Response):
    def __init__(self, code, status, data=None, message=None, error=False):
        self.code = code
        self.status = status
        self.data = data
        self.message = message

        result = {
            "code": code,
            "status": status,
            "data": data,
            "message": message
        }

        if error:
            result.pop('data', None)

        super().__init__(result, status)


class ErrorResponse(CommonResponse):
    def __init__(self, code, status, message):
        super().__init__(code=code, status=status, message=message, error=True)