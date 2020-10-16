from rest_framework.response import Response


class CommonResponse(Response):
    def __init__(self, code, status, data=None, message=None, headers=None):
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

        super().__init__(result, status, headers=headers)