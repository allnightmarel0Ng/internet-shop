import websockets
import json

from internal.app.authorization.usecase import AuthorizationUseCase
from internal.infrastructure.postgres import NoResultFound, MultipleResultsFound


class AuthorizationHandler:
    def __init__(self, use_case: AuthorizationUseCase):
        self.__use_case = use_case

    async def __handle(self, websocket, path):
        async for message in websocket:
            try:
                jwt = self.__use_case.authorize_entity(message)
                payload = {
                    "code": 200,
                    "jwt": jwt
                }
                await websocket.send(json.dumps(payload))
            except NoResultFound:
                await websocket.send(json.dumps({"code": 404, "error": "entity with such credentials wasn't found"}))
            except MultipleResultsFound:
                await websocket.send(json.dumps({"code": 404, "error": "too many entities with such credentials"}))
            except:
                await websocket.send(json.dumps({"code": 500, "error": "internal server error"}))

    async def start(self, port: int):
        server = await websockets.serve(self.__handle, "localhost", port)
        await server.wait_closed()
