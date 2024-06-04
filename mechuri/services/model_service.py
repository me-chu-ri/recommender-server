import numpy as np
import pandas as pd
import datetime
from django.db.models import QuerySet

from recommenders.ensembles.ensembler import Ensembler
from recommenders.models import KNN, EASEr
from recommenders.methods import Normalizers
from ..core.patterns.singleton_cls import Singleton
from ..dtos.requests.get_recommend_dto import GetRecommendDto
from ..models.models import PersonalKnnWeather, PersonalMenuPeriodicity, Menu, User, PersonalMenuInteraction, Group, \
    GroupMenuInteraction


class ModelService(metaclass=Singleton):
    def get_personal_recommend(self, data: GetRecommendDto):
        # get interactions
        interaction: pd.DataFrame = self._get_interaction_matrix()

        mat = interaction.values
        user_row = interaction.loc[[data.target_id], :].values
        ease_r_pred = self._get_ease_reverse_prediction(mat, user_row)

        # get weather knn
        weather_pred: list = self._get_weather_knn_prediction(data.target_id, data.temp, data.precip, data.humid)
        w_df: pd.DataFrame = pd.DataFrame(index=[data.target_id], columns=interaction.columns).fillna(0)
        for menu_id, cnt in weather_pred:
            w_df.loc[:, [menu_id]] = cnt

        # get periodicity
        period_pred: dict = self._get_periodicity_prediction(data.target_id)
        p_df: pd.DataFrame = pd.DataFrame(index=[data.target_id], columns=interaction.columns).fillna(0)
        for menu_id, value in period_pred.items():
            p_df.loc[:, [menu_id]] = value

        # combine
        ease_r = Normalizers.min_max_normalization(ease_r_pred)
        period = Normalizers.min_max_normalization(p_df.values)
        weather = Normalizers.min_max_normalization(w_df.values)

        result = self._get_recommend_score([ease_r, period, weather])
        max_idx = result.index(max(result))
        max_menu_id = interaction.columns[max_idx]

        # get the highest probability menu, return
        pass

    def get_group_recommend(self, data: GetRecommendDto):
        pass

    def _get_interaction_matrix(self) -> pd.DataFrame:
        menus: QuerySet = Menu.objects.all()

        users: QuerySet = User.objects.all()
        groups: QuerySet = Group.objects.all()

        personal_inter: list = list(PersonalMenuInteraction.objects.select_related('user', 'menu').all())
        group_inter: list = list(GroupMenuInteraction.objects.select_related('group', 'menu').all())

        target_list: list = [user.user_uuid for user in users] + [group.group_uuid for group in groups]

        menu_list: list = [menu.id for menu in menus]

        df: pd.DataFrame = pd.DataFrame(index=target_list, columns=menu_list).fillna(0.0)

        for inter in personal_inter:
            df.loc[inter.user.user_uuid, inter.menu.id] = inter.rating

        for inter in group_inter:
            df.loc[inter.group.group_uuid, inter.menu.id] = inter.rating

        return df  # row - user or group uuid, column - menu id

    def _get_weather_knn_prediction(self, target_id, temp, precip, humid, is_group: bool = False) -> list:
        # weathers: QuerySet = PersonalKnnWeather.objects.get_weather_selection(target_id)
        weathers: QuerySet
        if is_group:
            weathers = Group.objects.get_knn_weather_by_group_uuid(target_id)
        else:
            weathers = User.objects.get_knn_weather_by_user_uuid(target_id)
        x: list = []
        y: list = []
        for weather in weathers:
            x.append([weather.temp, weather.precip, weather.humid])
            y.append(weather.menu.id)

        knn: KNN = KNN(k_value=10, dim=3)
        knn.fit(np.array(x), np.array(y))
        weather_res: list = knn.predict(np.array([
            Normalizers.min_max_for_scalar(temp, -50, 50),
            Normalizers.min_max_for_scalar(precip, 0, 100),
            Normalizers.min_max_for_scalar(humid, 0, 100)
        ]))

        return weather_res  # [(menu_id, count), ...]

    def _get_periodicity_prediction(self, target_id, is_group: bool = False) -> dict:
        # periods: QuerySet = PersonalMenuPeriodicity.objects.get_menu_periodicity_set(target_id)
        periods: QuerySet
        if is_group:
            periods = Group.objects.get_menu_periodicity_by_group_uuid(target_id)
        else:
            periods = User.objects.get_menu_periodicity_by_user_uuid(target_id)
        days_after: dict = {item.menu.id: (datetime.datetime.now() - item.updated_at).days - item.periodicity for item in
                            periods}

        res = dict(zip(days_after.keys(), Normalizers.min_max_normalization(np.array(list(days_after.values())))))

        return res  # {menu_id: normalized days after last selected

    def _get_ease_reverse_prediction(self, mat, user_row):
        ease: EASEr = EASEr()
        ease.fit(mat)
        return ease.predict(user_row)

    def _get_recommend_score(self, factors: list) -> list:
        factors = np.array(factors)
        try:
            factors.shape[1]
        except IndexError:
            raise ValueError("factors must have the same shape")
        return list(Ensembler.basic_lists(factors))
