import jwt
import base64
import bcrypt

from internal.app.authorization.repository import AuthorizationRepository


class AuthorizationUseCase:
    def __init__(self, repository: AuthorizationRepository, jwt_secret_key: str):
        self.__repository = repository
        self.__jwt_secret_key = jwt_secret_key

    def authorize_entity(self, b64: str) -> str:
        try:
            decoded = base64.b64decode(b64, validate=True)
            decoded = decoded.decode()
        except:
            raise ValueError('invalid base64 format')

        tokens = decoded.split(':')
        if len(tokens) != 3:
            raise ValueError('invalid base64 format')

        entity_type = tokens[0]
        login = tokens[1]
        password = tokens[2]

        if entity_type == "shop":
            id, hash = self.__repository.authorize_shop(login)
        elif entity_type == "user":
            id, hash = self.__repository.authorize_user(login)
        else:
            raise ValueError('invalid entity type')

        if not bcrypt.checkpw(password.encode(), hash.encode()):
            raise ValueError('password mismatch')

        entity = {
            'id': id,
            'type': entity_type
        }

        return jwt.encode(entity, self.__jwt_secret_key)
