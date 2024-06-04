from rest_framework.request import Request

from ..core.utils.decorator_utils import get_request_from_args
from ..exceptions.type_exceptions import NotCallableError
from ..responses.error_response import ErrorResponse


def multi_methods(GET=None, POST=None, PUT=None, DELETE=None):
    def decorator(_):
        def target_method(*args, **kwargs):
            request: Request = get_request_from_args(*args)
            http_method: str = request.method
            try:
                if http_method == 'GET':
                    return GET(*args, **kwargs)
                elif http_method == 'POST':
                    return POST(*args, **kwargs)
                elif http_method == 'PUT':
                    return PUT(*args, **kwargs)
                elif http_method == 'DELETE':
                    return DELETE(*args, **kwargs)
            except TypeError:
                e = NotCallableError()
                return ErrorResponse.response(e, 500)
        return target_method
    return decorator
