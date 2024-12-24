from fastapi import HTTPException, status
from enum import Enum

from internal.app.profile.repository import *
from internal.infrastructure.postgres import NotFoundError, MultipleResultsFoundError


class ProfileType(Enum):
    SHOP = 1
    USER = 2
    PRODUCT = 3


class ProfileUseCase:
    def __init__(self, repository: ProfileRepository):
        self.__repository = repository

    @staticmethod
    def __encapsulate_entity(entity: Shop | User, is_public: bool):
        if is_public is False:
            return entity.__dict__

        if type(entity) is Shop:
            return {key: value for key, value in entity.__dict__.items() if key in ['id', 'name']}

        return {key: value for key, value in entity.__dict__.items() if key in ['id', 'name']}

    def get_profile_json(self, profile_type: ProfileType, entity_id: int, is_public: str) -> dict:
        is_public_boolean = False if is_public is None else str(is_public)
        try:
            if profile_type == ProfileType.SHOP:
                profile, products = self.__repository.get_shop_profile(
                    entity_id)
                response = {
                    "data": self.__encapsulate_entity(profile, is_public_boolean),
                    "products": [product.__dict__ for product in products]
                }
                return response
            elif profile_type == ProfileType.USER:
                profile, cart, paychecks = self.__repository.get_user_profile(
                    entity_id)
                response = {
                    "data": self.__encapsulate_entity(profile, is_public_boolean)
                }
                if is_public_boolean is False:
                    response["cart"] = [item.__dict__ for item in cart]
                    response["paychecks"] = [
                        {"common": item[0], "products": item[1]} for item in paychecks]
                return response

            profile, category_name, shop_name = self.__repository.get_product_profile(
                entity_id)
            response = {
                "data": profile.__dict__,
                "category": category_name,
                "shop": shop_name
            }
            return response

        except (NotFoundError, MultipleResultsFoundError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid id of profile')
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='db error')
