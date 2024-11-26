from fastapi import Header, HTTPException, status, APIRouter

from internal.app.authorization.usecase import AuthorizationUseCase
from internal.infrastructure.postgres import NoResultFound, MultipleResultsFound

class AuthorizationHandler:
    def __init__(self, use_case: AuthorizationUseCase):
        self.__use_case = use_case
        self.router = APIRouter()
        self.router.add_api_route(
            "/authentication", self.authentication, methods=["GET"])

    def authentication(self, authorization: str = Header(None)):
        if not authorization and authorization.count('Basic ') < 1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="authorization header is missing or not Basic")

        b64 = authorization.replace('Basic ', '')
        try:
            jwt = self.__use_case.authorize_entity(b64)
        except ValueError as v:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(v))
        except (NoResultFound, MultipleResultsFound) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        return {'code': status.HTTP_200_OK, 'jwt': jwt}
