import numpy as np
import pandas as pd
from django.db.models import QuerySet
from django.utils import timezone

from recommenders.ensembles.ensembler import Ensembler
from recommenders.models import KNN, EASEr, EMA
from recommenders.methods import Normalizers
from ..core.patterns.singleton_cls import Singleton
from ..dtos.requests.get_recommend_dto import GetRecommendDto
from ..dtos.requests.post_interaction_dto import PostInteractionDto
from ..dtos.responses.common_response import CommonResponse
from ..dtos.responses.menu_dto import MenuDto
from ..models.models import Menu, User, PersonalMenuInteraction, Group, \
    GroupMenuInteraction


class ModelService(metaclass=Singleton):
    def get_personal_recommend(self, data: GetRecommendDto):
        menu_list = self._get_recommend(data, False)
        recommended_menus = [MenuDto.from_entity(entity) for entity in Menu.objects.filter_menus_by_ids(menu_list)]
        return recommended_menus

    def get_group_recommend(self, data: GetRecommendDto):
        menu_list = self._get_recommend(data, True)
        recommended_menus = [MenuDto.from_entity(entity) for entity in Menu.objects.filter_menus_by_ids(menu_list)]
        return recommended_menus

    def post_interaction(self, data: PostInteractionDto, is_group: bool):
        if is_group:
            model = Group
            target = Group.objects.get(group_uuid=data.target_id)
            entity = GroupMenuInteraction
        else:
            model = User
            target = User.objects.get(user_uuid=data.target_id)
            entity = PersonalMenuInteraction

        interactions = model.objects.get_interaction(data.target_id, data.menu_id)

        if len(interactions) == 0:
            menu: Menu = Menu.objects.get(id=data.menu_id)
            entity.objects.create(
                target,
                menu,
                data.rating
            )
            return CommonResponse(True, 'successfully created menu rating')

        interaction = interactions[0]
        ema = EMA()
        rating = ema.update(interaction.rating, data.rating)

        interaction.rating = rating
        interaction.save(update_fields=["rating"])

        return CommonResponse(True, 'successfully updated menu rating')

    def delete_interaction_personal(self):
        pass

    def delete_interaction_group(self):
        pass

    def select_menu_personal(self):
        pass

    def select_menu_group(self):
        pass

    def _get_recommend(self, data: GetRecommendDto, is_group):
        interaction_df, target_series = self._get_interaction_matrix(data.target_id)

        # get interactions
        mat = interaction_df.values
        user_row = interaction_df.loc[[data.target_id], :].values
        ease_r_pred: np.ndarray = self._get_ease_reverse_prediction(mat, user_row)

        #
        """
        처음 좋아요 하면 interaction table에 데이터 생기고,
        좋아요를 한거면 위 조건에 의해 더이상 추천될 수 없음
        위 조건을 추가하지 않으면 데이터가 작아서인지 큰 가중치를 가져 해당 메뉴만 계속 추천됨
        
        상호작용이 있고 난 후엔 다른 메뉴를 추천해줘야함
        
        last_interaction 값을 이용해서 한번 상호작용이 있고 나면 금방 다시 추천될 확률은 0, 시간이 지남에 따라 올라가도록
        
        use target_series to use time information after last interaction
        """

        """
        Temporal implementation
        """
        not_interacted = interaction_df.loc[data.target_id, :].apply(lambda x: x < 0.5)  # to remove (interaction > 0.5) (1 ~ -1)
        exc_interacted: np.ndarray = not_interacted.astype(float).values * ease_r_pred

        ## just remove already interacted menus
        ease_r_pred: np.ndarray = exc_interacted

        # print([interaction.columns[i] for i in np.argsort(ease_r_pred)])

        ## weighted sum
        # ease_r_pred = Ensembler.weighted_sum(np.array([exc_interacted, ease_r_pred]), np.array([[0.7], [0.3]]))
        #

        # get weather knn
        weather_pred: list = self._get_weather_knn_prediction(data.target_id, data.temp, data.precip, data.humid,
                                                              is_group)
        w_df: pd.Series = pd.Series(index=interaction_df.columns).fillna(0)
        for menu_id, cnt in weather_pred:
            w_df.loc[menu_id] = cnt

        # get periodicity
        period_pred: dict = self._get_periodicity_prediction(data.target_id, is_group)
        p_df: pd.Series = pd.Series(index=interaction_df.columns).fillna(0)
        for menu_id, value in period_pred.items():
            p_df.loc[menu_id] = value

        # combine
        ease_r = Normalizers.min_max_normalization(ease_r_pred)
        period = Normalizers.min_max_normalization(p_df.values)
        weather = Normalizers.min_max_normalization(w_df.values)

        result = self._get_recommend_score([ease_r, period, weather])

        max_ids = np.where(result == np.max(result))[0]
        max_menus = [interaction_df.columns[idx] for idx in max_ids]

        # get the highest probability menu, return
        return max_menus

    def _get_interaction_matrix(self, target_uuid: str = '') -> tuple:
        menus: QuerySet = Menu.objects.all()

        users: QuerySet = User.objects.all()
        groups: QuerySet = Group.objects.all()

        personal_inter: list = list(PersonalMenuInteraction.objects.select_related('user', 'menu').all())
        group_inter: list = list(GroupMenuInteraction.objects.select_related('group', 'menu').all())

        target_list: list = [user.user_uuid for user in users] + [group.group_uuid for group in groups]

        menu_list: list = [menu.id for menu in menus]

        df: pd.DataFrame = pd.DataFrame(index=target_list, columns=menu_list).fillna(0.0)

        inter_series: pd.Series = pd.Series(index=menu_list).fillna(0)

        for inter in personal_inter:
            df.loc[inter.user.user_uuid, inter.menu.id] = inter.rating
            if inter.user.user_uuid == target_uuid:
                inter_series[inter.menu.id] = timezone.now() - inter.last_interacted_at

        for inter in group_inter:
            df.loc[inter.group.group_uuid, inter.menu.id] = inter.rating
            if inter.group.group_uuid == target_uuid:
                inter_series[inter.menu.id] = timezone.now() - inter.last_interacted_at

        return df, inter_series  # row - user or group uuid, column - menu id

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

        if len(periods) == 0:
            return {}

        days_after: dict = {item.menu.id: (timezone.now() - item.updated_at).days - item.periodicity for item
                            in
                            periods}

        res = dict(zip(days_after.keys(), Normalizers.min_max_normalization(np.array(list(days_after.values())))))

        return res  # {menu_id: normalized days after last selected

    def _get_ease_reverse_prediction(self, mat, user_row):
        ease: EASEr = EASEr(_lambda=100)
        ease.fit(mat)
        return ease.predict(user_row)

    def _get_recommend_score(self, factors: list) -> np.ndarray:
        factors = np.array(factors)
        try:
            factors.shape[1]
        except IndexError:
            raise ValueError("factors must have the same shape")
        return Ensembler.weighted_sum(factors, np.array([[0.4], [0.3], [0.3]]))
