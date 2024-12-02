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
        self.router.add_api_route("/deposit/", self.deposit, methods=["POST"])
    
    def __init__(self, use_case: GatewayUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):
        @self.router.get("/login")
        async def login(authorization: str = Header(None)):
            return self.login(authorization)

        @self.router.post("/logout")
        async def logout(authorization: str = Header(None)):
            return self.logout(authorization)

        @self.router.post("/deposit")
        async def deposit(deposit: Deposit = Body(...), authorization: str = Header(...)):
            return self.deposit(deposit, authorization)
        
        @self.router.get("/profile")
        async def profile(authorization: str = Header(...)):
            return self.profile(authorization)

    def login(self, authorization: str):
        code, data = self.__use_case.authentication(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=data['detail'])
        return {'jwt': data['jwt']}

    def logout(self, authorization: str):
        code, body = self.__use_case.logout(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=body['detail'])
        return

    def deposit(self, deposit: Deposit, authorization: str):
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

    def profile(self, authorization: str):
        try:
            return self.__use_case.profile(auth_header=authorization)
        except HTTPException as e:
            raise e
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected_error')