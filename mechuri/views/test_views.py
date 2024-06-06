import random

from django.http import HttpResponse

from mechuri.models.models import User, Group, Menu, PersonalMenuInteraction, GroupMenuInteraction
from mechuri.responses.error_response import ErrorResponse


def test_create(request):
    users = []
    groups = []
    for i in range(10):
        user = User.objects.create(
            user_uuid=f'test_user{i}',
            email=f'test{i}@gmail.com',
            password='password',
            nickname=f'test{i}'
        )

        group = Group.objects.create(
            group_uuid=f'test_group{i}',
            name='test_group'
        )
        users.append(user)
        groups.append(group)

    for i in range(len(users)):
        if i == 0:
            m = [2, 3, 9, 57, 150, 192, 241, 272, 277, 280, 313]
        else:
            m = [random.randint(1, 404) for _ in range(10)]
        for menu_id in m:
            menu = Menu.objects.get(id=menu_id)
            PersonalMenuInteraction.objects.create(
                user=users[i],
                menu=menu,
                rating=1
            )

    for i in range(len(groups)):
        # if i == 0:
        #     m = [2, 3, 57, 241, 277, 313, 274, 359, 383, 393]
        # else:
        #     m = [random.randint(1, 404) for _ in range(10)]
        m = [random.randint(1, 404) for _ in range(10)]

        for menu_id in m:
            menu = Menu.objects.get(id=menu_id)
            GroupMenuInteraction.objects.create(
                group=groups[i],
                menu=menu,
                rating=1
            )

    return HttpResponse('good')


def test_delete(request):
    try:
        for i in range(10):
            user = User.objects.get(user_uuid=f'test_user{i}')
            group = Group.objects.get(group_uuid=f'test_group{i}')

            GroupMenuInteraction.objects.filter(group=group).delete()
            PersonalMenuInteraction.objects.filter(user=user).delete()
            user.delete()
            group.delete()
        return HttpResponse('good')
    except Exception as e:
        return ErrorResponse.response(e)
