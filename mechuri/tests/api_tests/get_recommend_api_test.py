from django.test import TestCase, Client
from ...models.models import User, Group, GroupMenuInteraction, PersonalMenuInteraction, Menu


client = Client()


class GetRecommendAPITest(TestCase):
    def setUp(self):
        self.query_params = '?targetId=test_uuid&temp=15.4&precip=20&humid=30'

        self.response_data = {
            'probability': 34.4,
            'menu': {
                'name': '초밥',
                'nutrient': {
                    'energy': 134.0,
                    'cabs': 14.4,
                    'prot': 4.3,
                    'fat': 23.6,
                    'sug': 13.1,
                    'nat': 31.2
                }
            }
        }

        self.user = User.objects.create(
            user_uuid='test_uuid',
            email='test@gmail.com',
            password='password',
            nickname='test'
        )

        self.group = Group.objects.create(
            group_uuid='test_group',
            name='test_group'
        )

        menus = [2, 3, 9, 57, 150, 192, 241, 272, 277, 280, 313]
        for menu_id in menus:
            menu = Menu.objects.get(id=menu_id)
            PersonalMenuInteraction.objects.create(
                user=self.user,
                menu=menu,
                rating=1
            )

        for menu_id in menus[:9]:
            menu = Menu.objects.get(id=menu_id)
            GroupMenuInteraction.objects.create(
                group=self.group,
                menu=menu,
                rating=1
            )

    def tearDown(self):
        self.user.delete()
        self.group.delete()
        GroupMenuInteraction.objects.filter(group=self.group).delete()
        PersonalMenuInteraction.objects.filter(user=self.user).delete()

    def test_personal_recommend(self):
        res = client.get(f'/model/v1/menu/personal{self.query_params}', content_type='application/json')
        print(res)
        self.assertEqual(res, self.response_data)

    # def test_group_recommend(self):
    #     res = client.get(f'/model/v1/menu/group{self.query_params}', content_type='application/json')
    #     self.assertEqual(res, self.response_data)
