from typing import Type, Tuple
from django.http import QueryDict
from rest_framework.request import Request

from ..core.utils.decorator_utils import get_request_from_args
from ..dtos.abstract_dto import Dto
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import DeserializeDataTypeError, RequestDataConversionError, DynamicTypeError, DtoFieldTypeError
from ..responses.error_response import ErrorResponse


def deserialize(view_method):
    def __get_raw_query_params(params: QueryDict) -> dict:
        query_params: dict = dict()
        for key, value in params.items():
            if len(value) == 1:
                query_params[key] = value[0]
            else:
                query_params[key] = value
        return query_params

    def __get_req_data(request: Request) -> dict:
        data: dict = request.data
        data.update(__get_raw_query_params(request.query_params))
        return data

    def __get_target_datatype_pair() -> Tuple[str, Type[Dto]]:
        for arg in view_method.__annotations__.items():
            if issubclass(arg[1], Dto):
                return arg

    def pass_deserialized_obj(*args, **kwargs):
        try:
            key, _type = __get_target_datatype_pair()

            request: Request = get_request_from_args(*args)
            data: dict = __get_req_data(request)

            deserialized_obj: Dto = _type.deserialize(data)

            kwargs[key] = deserialized_obj
            return view_method(*args, **kwargs)
        except MissingFieldError as e:
            return ErrorResponse.response(e, 400)
        except RequestDataConversionError as e:
            return ErrorResponse.response(e, 400)
        except DynamicTypeError as e:
            return ErrorResponse.response(e, 500)
        except DtoFieldTypeError as e:
            return ErrorResponse.response(e, 500)
        except DeserializeDataTypeError as e:
            return ErrorResponse.response(e, 500)
        except Exception as e:
            return ErrorResponse.response(e, 500)

    pass_deserialized_obj.__annotations__ = view_method.__annotations__
    return pass_deserialized_obj
