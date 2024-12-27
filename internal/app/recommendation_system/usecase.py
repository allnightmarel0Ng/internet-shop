from internal.app.recommendation_system.repository import *
from ml.recommendation_system.model import RecommendationSystem


class RecommendationSystemUseCase:
    def __init__(self, ml: RecommendationSystem, repo: RecommendationSystemRepository):
        self.__ml = ml
        self.__repo = repo

    def predict(self, user_id: int, count: int):
        if user_id == 0:
            return self.__repo.get_most_popular(count)

        reviewed = self.__repo.get_user_products_reviewed(user_id)
        if not reviewed:
            return self.__repo.get_most_popular(count)

        ids = self.__ml.recommend_items(user_id, reviewed, count)
        return [item.__dict__ for item in self.__repo.get_products_by_ids(ids)]
