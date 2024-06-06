from django.urls import path
from .views import base_views, model_views, test_views


urlpatterns = [
    path('', base_views.index),
    path('model/v1/menu/personal', model_views.recommend_methods_personal),
    path('model/v1/menu/group', model_views.recommend_methods_group),
    path('model/v1/menu/select/persnal', model_views.post_selection_personal),
    path('model/v1/menu/select/group', model_views.post_selection_group),

    path('test/create', test_views.test_create),
    path('test/delete', test_views.test_delete)
]
