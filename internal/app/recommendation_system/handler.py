from fastapi import APIRouter

from internal.app.recommendation_system.usecase import RecommendationSystemUseCase


class RecommendationSystemHandler:
    def __init__(self, use_case: RecommendationSystemUseCase):
        self.__use_case = use_case
        self.router = APIRouter()

        self.router.add_api_route(
            "/predict/{user_id}", self.predict, methods=["GET"])

    async def predict(self, user_id: int, count: str = None):
        count = int(count) if count is not None else 10
        return self.__use_case.predict(user_id, count)
