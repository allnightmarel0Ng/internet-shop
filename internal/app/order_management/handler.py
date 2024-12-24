import asyncio
import threading
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

import grpc

from internal.app.order_management.usecase import *

import internal.protos.order_management.order_management_pb2 as order_management_pb2
import internal.protos.order_management.order_management_pb2_grpc as order_management_pb2_grpc


class OrderManagementHandler(order_management_pb2_grpc.OrderManagementServiceServicer):
    def __init__(self, use_case: OrderManagementUseCase):
        self.use_case = use_case

    def AddProduct(self, request, context):
        def entrypoint():
            asyncio.run(self.use_case.add_to_cart(
                request.user_id, request.product_id))

        t = threading.Thread(target=entrypoint, daemon=True)
        t.start()
        return order_management_pb2.OrderOperationResponse(status_code=200)

    def DeleteProduct(self, request, context):
        def entrypoint():
            asyncio.run(self.use_case.delete_from_cart(
                request.user_id, request.product_id))

        t = threading.Thread(target=entrypoint, daemon=True)
        t.start()
        return order_management_pb2.OrderOperationResponse(status_code=200)


def serve(use_case: OrderManagementUseCase, port: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = OrderManagementHandler(use_case)
    order_management_pb2_grpc.add_OrderManagementServiceServicer_to_server(
        servicer, server)
    server.add_insecure_port(f"0.0.0.0:{port}")
    server.start()
    server.wait_for_termination()
