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


class GroupMenuInteractionManager(Manager):
    use_for_related_fields = True


class PersonalKnnLocManager(Manager):
    use_for_related_fields = True


class GroupKnnLocManager(Manager):
    use_for_related_fields = True


class MenuManager(Manager):
    use_for_related_fields = True


class UserManager(Manager):
    use_for_related_fields = True

    def get_knn_weather_by_user_uuid(self, uuid):
        user = self.get(user_uuid=uuid)
        return user.personalknnweather_set.select_related('user', 'menu').all()

    def get_menu_periodicity_by_user_uuid(self, uuid) -> QuerySet:
        user =  self.get(user_uuid=uuid)
        return user.personalmenuperiodicity_set.select_related('user', 'menu').all()


class GroupManager(Manager):
    use_for_related_fields = True

    def get_knn_weather_by_group_uuid(self, uuid):
        group = self.get(group_uuid=uuid)
        return group.groupknnweather_set.select_related('group', 'menu').all()

    def get_menu_periodicity_by_group_uuid(self, uuid):
        group = self.get(group_uuid=uuid)
        return group.groupmenuperiodicity_set.select_related('group', 'menu').all()
