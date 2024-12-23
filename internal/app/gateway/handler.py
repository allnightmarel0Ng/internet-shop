from fastapi import Header, Body, HTTPException, APIRouter, status
from pydantic import BaseModel

from internal.app.gateway.usecase import GatewayUseCase


class Deposit(BaseModel):
    money: int


class GatewayHandler:
    def __init__(self, use_case: GatewayUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.router.add_api_route("/api/login", self.login, methods=["GET"])
        self.router.add_api_route("/api/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/api/deposit", self.deposit, methods=["POST"])
        self.router.add_api_route("/api/profile/self", self.profile_self, methods=["GET"])
        self.router.add_api_route("/api/add/{product_id}", self.add_to_cart, methods=["POST"])
        self.router.add_api_route("/api/delete/{product_id}", self.delete_from_cart, methods=["DELETE"])

    async def login(self, authorization: str = Header(None)):
        code, data = self.__use_case.authentication(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=data['detail'])
        return {'jwt': data['jwt']}

    async def logout(self, authorization: str = Header(None)):
        code, body = self.__use_case.logout(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=body['detail'])

    async def deposit(self, deposit: Deposit, authorization: str = Header(None)):
        if deposit.money <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='unable to deposit non positive amount of money')

        if not authorization or authorization.count('Bearer ') != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid authorization format')

        code, detail = self.__use_case.deposit(
            deposit.money, auth_header=authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=detail['detail'])

    async def profile_self(self, authorization: str = Header(None)):
        return self.__use_case.profile(auth_header=authorization)

    async def add_to_cart(self, product_id: int, authorization: str = Header(None)):
        self.__use_case.add_to_cart(auth_header=authorization, product_id=product_id)

    async def delete_from_cart(self, product_id: int, authorization: str = Header(None)):
        self.__use_case.delete_from_cart(auth_header=authorization, product_id=product_id)
