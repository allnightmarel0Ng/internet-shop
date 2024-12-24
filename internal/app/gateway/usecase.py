import grpc
import requests
import json

from fastapi import status, HTTPException

from internal.infrastructure.kafka import Producer
from internal.protos.order_management.order_management_pb2_grpc import OrderManagementServiceStub
from internal.protos.order_management.order_management_pb2 import OrderOperationRequest


class GatewayUseCase:
    def __init__(self, producer: Producer, authorization_port: str, profile_port: str, order_management_port: str):
        self.__producer = producer
        self.__authorization_port = authorization_port
        self.__profile_port = profile_port
        self.__order_management_port = order_management_port

    @staticmethod
    def __fetch_get(url):
        response = requests.get(url)
        response_data = response.json()
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code,
                                detail=response_data['detail'])
        return response_data

    def __authorization(self, auth_header: str) -> dict:
        response = requests.get(
            f"http://authorization:{self.__authorization_port}/authorization", headers={'Authorization': auth_header})
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='unable to authorize the request')
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

    def profile_self(self, auth_header: str):
        response_data = self.__authorization(auth_header)
        return self.__fetch_get(f"http://profile:{self.__profile_port}/{response_data['type']}/{response_data['id']}")

    def profile_other(self, entity_type: str, entity_id: int):
        return self.__fetch_get(f"http://profile:{self.__profile_port}/{entity_type}/{entity_id}?is_public=True")

    def add_to_cart(self, auth_header: str, product_id: int):
        self.__cart_operation(
            to_add=True, auth_header=auth_header, product_id=product_id)

    def delete_from_cart(self, auth_header: str, product_id: int):
        self.__cart_operation(
            to_add=False, auth_header=auth_header, product_id=product_id)

    def __cart_operation(self, to_add: bool, auth_header: str, product_id: int):
        response_data = self.__authorization(auth_header)

        with grpc.insecure_channel(f"order_management:{self.__order_management_port}") as channel:
            stub = OrderManagementServiceStub(channel)

            if to_add is True:
                stub.AddProduct(OrderOperationRequest(
                    user_id=response_data['id'], product_id=product_id))
            else:
                stub.DeleteProduct(OrderOperationRequest(
                    user_id=response_data['id'], product_id=product_id))
