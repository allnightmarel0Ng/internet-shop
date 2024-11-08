import jwt
import base64
import json

from internal.app.authorization.repository import AuthorizationRepository


class AuthorizationUseCase:
    def __init__(self, repository: AuthorizationRepository, jwt_secret_key: str):
        self.__repository = repository
        self.__jwt_secret_key = jwt_secret_key

    def authorize_entity(self, json_data: str) -> str:
        data = json.loads(json_data)
        decoded_credentials = base64.b64decode(
            data["base64"]).decode().split(":")
        entity_type = data["type"]

        entity = dict()
        if entity_type == "shop":
            entity = self.__repository.authorize_shop(
                decoded_credentials[0], decoded_credentials[1]).to_dict()
        elif entity_type == "user":
            entity = self.__repository.authorize_user(
                decoded_credentials[0], decoded_credentials[1]).to_dict()

        entity["type"] = entity_type

        return jwt.encode(entity, self.__jwt_secret_key)
