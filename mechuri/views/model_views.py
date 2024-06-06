from django.http import HttpResponse
from rest_framework.decorators import api_view

from ..decorators.multi_method_decorator import multi_methods
from ..services.model_service import ModelService
from ..decorators.deserialize_decorator import deserialize
from ..responses.dto_response import DtoResponse
from ..responses.error_response import ErrorResponse
from ..dtos.requests.get_recommend_dto import GetRecommendDto
from ..dtos.requests.post_interaction_dto import PostInteractionDto
from ..dtos.requests.post_selection_dto import PostSelectionDto
from ..dtos.requests.delete_interaction_dto import DeleteInteractionDto

model_service = ModelService()


@deserialize
def get_recommend_personal(request, data: GetRecommendDto):
    try:
        res = model_service.get_personal_recommend(data)
        return DtoResponse.response(res)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@deserialize
def get_recommend_group(request, data: GetRecommendDto):
    try:
        res = model_service.get_group_recommend(data)
        return DtoResponse.response(res)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@deserialize
def post_interaction_personal(request, data: PostInteractionDto):
    try:
        res = model_service.post_interaction(data, False)
        return DtoResponse.response(res)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@deserialize
def post_interaction_group(request, data: PostInteractionDto):
    try:
        res = model_service.post_interaction(data, True)
        return DtoResponse.response(res)
    except Exception as e:
        return ErrorResponse.response(e, 500)


@deserialize
def delete_interaction_personal(request, data: DeleteInteractionDto):
    try:
        pass
    except Exception as e:
        return ErrorResponse.response(e, 500)


@deserialize
def delete_interaction_group(request, data: DeleteInteractionDto):
    try:
        pass
    except Exception as e:
        return ErrorResponse.response(e, 500)


# GET model/v1/menu/select/personal
@deserialize
def post_selection_personal(request, data: PostSelectionDto):
    try:
        pass
    except Exception as e:
        return ErrorResponse.response(e, 500)


# GET model/v1/menu/select/group
@deserialize
def post_selection_group(request, data: PostSelectionDto):
    try:
        pass
    except Exception as e:
        return ErrorResponse.response(e, 500)


# [GET, POST, DELETE] model/v1/menu/personal
@api_view(['GET', 'POST', 'DELETE'])
@multi_methods(GET=get_recommend_personal, POST=post_interaction_personal, DELETE=delete_interaction_personal)
def recommend_methods_personal(request):
    return HttpResponse('')


# [GET, POST, DELETE] model/v1/menu/group
@api_view(['GET', 'POST', 'DELETE'])
@multi_methods(GET=get_recommend_group, POST=post_interaction_group, DELETE=delete_interaction_group)
def recommend_methods_group(request):
    return HttpResponse('')
