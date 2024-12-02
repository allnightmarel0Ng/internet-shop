import requests
import json

from fastapi import status, HTTPException

from internal.infrastructure.kafka import Producer


class GatewayUseCase:
    def __init__(self, producer: Producer, authorization_port: int, profile_port: int):
        self.__producer = producer
        self.__authorization_port = authorization_port
        self.__profile_port = profile_port

    def __authorization(self, auth_header: str) -> dict:
        response = requests.get(
            f"http://authorization:{self.__authorization_port}/authorization", headers={'Authorization': auth_header})
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unable to authorize the request')
        return response.json()

    def authentication(self, auth_header: str):
        response = requests.get(
            f"http://authorization:{self.__authorization_port}/authentication", headers={'Authorization': auth_header})
        return response.status_code, response.json()

    def logout(self, auth_header: str):
        response = requests.post(
            f"http://authorization:{self.__authorization_port}/logout", headers={'Authorization': auth_header})
        return response.status_code, response.json()

    def deposit(self, money: int, auth_header: str):
        response_data = self.__authorization(auth_header)

        if response_data['type'] != 'user':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='shops cant deposit any money')

        msg_dict: dict = {
            'type': 'deposit',
            'userID': response_data['id'],
            'diff': money
        }

        self.__producer.produce('money_operations', json.dumps(msg_dict))
        return status.HTTP_200_OK, 'success'

    def profile(self, auth_header: str):
        response_data = self.__authorization(auth_header)
        
        response = requests.get(f"http://profile:{self.__profile_port}/{response_data['type']}/{response_data['id']}")
        response_data = response.json()
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code, detail=response_data['detail'])
        return response_data
            