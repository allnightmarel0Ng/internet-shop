import asyncio
from concurrent import futures

import grpc

from internal.app.order_management.usecase import *

import internal.protos.order_management.order_management_pb2 as order_management_pb2
import internal.protos.order_management.order_management_pb2_grpc as order_management_pb2_grpc


class OrderManagementHandler(order_management_pb2_grpc.OrderManagementServiceServicer):
    use_case: OrderManagementUseCase

    def serve(self, use_case: OrderManagementUseCase, port):
        self.use_case = use_case

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        order_management_pb2_grpc.add_OrderManagementServiceServicer_to_server(self, server)
        server.add_insecure_port(f"0.0.0.0:{port}")
        server.start()
        server.wait_for_termination()

    def AddProduct(self, request, context):
        asyncio.create_task(self.use_case.add_to_cart(
            request.user_id, request.product_id))
        return order_management_pb2.OrderOperationResponse(status_code=200)

    def DeleteProduct(self, request, context):
        asyncio.create_task(self.use_case.add_to_cart(
            request.user_id, request.product_id))
        return order_management_pb2.OrderOperationResponse(status_code=200)
