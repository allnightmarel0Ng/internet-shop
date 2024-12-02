from fastapi import Header, HTTPException, status, APIRouter

from internal.app.authorization.usecase import AuthorizationUseCase
from internal.infrastructure.postgres import NotFoundError, MultipleResultsFoundError


class AuthorizationHandler:
    def __init__(self, use_case: AuthorizationUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.router.add_api_route(
            "/authentication", self.authentication, methods=["GET"])
        self.router.add_api_route(
            "/authorization", self.authorization, methods=["GET"])
        self.router.add_api_route(
            "/logout", self.logout, methods=["POST"])

    def authentication(self, authorization: str = Header(None)):
        if not authorization and authorization.count('Basic ') < 1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="authorization header missing or not Basic")

        b64 = authorization.replace('Basic ', '')
        try:
            jwt = self.__use_case.authenticate_entity(b64)
        except (NotFoundError, MultipleResultsFoundError) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        return {'jwt': jwt}

    def authorization(self, authorization: str = Header(None)):
        if not authorization and authorization.count('Bearer ') < 1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="authorization header missing or not Bearer")

        json_web_token = authorization.replace('Bearer ', '')
        entity_id, entity_type = self.__use_case.authorize_entity(
            json_web_token)

        return {'id': entity_id, 'type': entity_type}

    def logout(self, authorization: str = Header(None)):
        if not authorization and authorization.count('Bearer ') < 1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="authorization header missing or not Bearer")

        json_web_token = authorization.replace('Bearer ', '')
        self.__use_case.logout_entity(json_web_token)
