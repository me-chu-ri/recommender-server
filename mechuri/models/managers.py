from django.db.models import Manager, QuerySet


class PersonalKnnWeatherManager(Manager):
    use_for_related_fields = True


class GroupKnnWeatherManager(Manager):
    use_for_related_fields = True


class PersonalMenuPeriodicityManager(Manager):
    use_for_related_fields = True


class GroupMenuPeriodicityManager(Manager):
    use_for_related_fields = True


class PersonalMenuInteractionManager(Manager):
    use_for_related_fields = True

    def create(self, user, menu, rating: float):
        return super().create(
            user=user,
            menu=menu,
            rating=rating
        )


class GroupMenuInteractionManager(Manager):
    use_for_related_fields = True

    def create(self, group, menu, rating: float):
        return super().create(
            group=group,
            menu=menu,
            rating=rating
        )


class PersonalKnnLocManager(Manager):
    use_for_related_fields = True


class GroupKnnLocManager(Manager):
    use_for_related_fields = True


class MenuManager(Manager):
    use_for_related_fields = True

    def filter_menus_by_ids(self, ids: list):
        return self.filter(id__in=ids).select_related('nutrient')


class UserManager(Manager):
    use_for_related_fields = True

    def get_knn_weather_by_user_uuid(self, uuid):
        user = self.get(user_uuid=uuid)
        return user.personalknnweather_set.select_related('user', 'menu').all()

    def get_menu_periodicity_by_user_uuid(self, uuid) -> QuerySet:
        user = self.get(user_uuid=uuid)
        return user.personalmenuperiodicity_set.select_related('user', 'menu').all()

    def get_interaction(self, target_uuid, menu_id):
        user = self.get(user_uuid=target_uuid)
        return user.personalmenuinteraction_set.filter(menu=menu_id).select_related('user', 'menu')


class GroupManager(Manager):
    use_for_related_fields = True

    def get_knn_weather_by_group_uuid(self, uuid):
        group = self.get(group_uuid=uuid)
        return group.groupknnweather_set.select_related('group', 'menu').all()

    def get_menu_periodicity_by_group_uuid(self, uuid):
        group = self.get(group_uuid=uuid)
        return group.groupmenuperiodicity_set.select_related('group', 'menu').all()

    def get_interaction(self, target_uuid, menu_id):
        group = self.get(group_uuid=target_uuid)
        return group.groupmenuinteraction_set.filter(menu=menu_id).select_related('group', 'menu')
