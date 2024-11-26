from fastapi import Header, HTTPException, APIRouter, status

from internal.app.gateway.usecase import GatewayUseCase


class GatewayHandler:
    def __init__(self, use_case: GatewayUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.router.add_api_route("/login", self.login, methods=["GET"])

    def login(self, authorization=Header(None)):
        code, data = self.__use_case.authentication(authorization)
        if code == status.HTTP_200_OK:
            return {'jwt': data['jwt']}
        else:
            raise HTTPException(status_code=code, detail=data['detail'])
