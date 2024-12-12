from fastapi import Header, Body, HTTPException, APIRouter, status
from pydantic import BaseModel

from internal.app.gateway.usecase import GatewayUseCase


class Deposit(BaseModel):
    money: int


class GatewayHandler:
    def __init__(self, use_case: GatewayUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.router.add_api_route("/login", self.login, methods=["GET"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/deposit", self.deposit, methods=["POST"])
        self.router.add_api_route("/profile", self.deposit, methods=["GET"])

    async def login(self, authorization: str):
        code, data = self.__use_case.authentication(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=data['detail'])
        return {'jwt': data['jwt']}

    async def logout(self, authorization: str):
        code, body = self.__use_case.logout(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=body['detail'])
        return

    async def deposit(self, deposit: Deposit, authorization: str):
        if deposit.money <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='unable to deposit non positive amount of money')

        if not authorization or authorization.count('Bearer ') != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid authorization format')
        try:
            code, detail = self.__use_case.deposit(
                deposit.money, auth_header=authorization)
            if code != status.HTTP_200_OK:
                raise HTTPException(status_code=code, detail=detail['detail'])
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error')

    async def profile(self, authorization: str):
        try:
            return self.__use_case.profile(auth_header=authorization)
        except HTTPException as e:
            raise e
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected_error')