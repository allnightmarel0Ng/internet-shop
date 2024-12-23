import json
from fastapi import HTTPException, status
from enum import Enum

from internal.app.profile.repository import *
from internal.infrastructure.postgres import NotFoundError, MultipleResultsFoundError


class ProfileType(Enum):
    SHOP = 1
    USER = 2


class ProfileUseCase:
    def __init__(self, repository: ProfileRepository):
        self.__repository = repository

    def get_profile_json(self, profile_type: ProfileType, entity_id: int) -> dict:
        try:
            if profile_type == ProfileType.SHOP:
                profile = self.__repository.get_shop_profile(entity_id)
                return profile.__dict__
            else:
                profile = self.__repository.get_user_profile(entity_id)
                return profile.__dict__
        except (NotFoundError, MultipleResultsFoundError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid id of profile')
        except Exception as e:
            print(str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='db error')
