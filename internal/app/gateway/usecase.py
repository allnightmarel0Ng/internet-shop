import requests


class GatewayUseCase:
    def __init__(self, authorization_port: int):
        self.__authorization_port = authorization_port

    def authentication(self, auth_header: str):
        response = requests.get(
            f"http://authorization:{self.__authorization_port}/authentication", headers={'Authorization': auth_header})
        return (response.status_code, response.json())
