from fastapi import APIRouter

from internal.app.profile.usecase import ProfileUseCase, ProfileType


class ProfileHandler:
    def __init__(self, use_case: ProfileUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.router.add_api_route("/shop/{shop_id}", self.shop_profile, methods=["GET"])
        self.router.add_api_route("/user/{user_id}", self.user_profile, methods=["GET"])
    
    def shop_profile(self, shop_id):
        return self.__use_case.get_profile_json(ProfileType.SHOP, shop_id)
    
    def user_profile(self, user_id):
        return self.__use_case.get_profile_json(ProfileType.USER, user_id)