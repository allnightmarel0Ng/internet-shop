# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import order_management_pb2 as order__management__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in order_management_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class OrderManagementServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddProduct = channel.unary_unary(
            '/OrderManagementService/AddProduct',
            request_serializer=order__management__pb2.OrderOperationRequest.SerializeToString,
            response_deserializer=order__management__pb2.OrderOperationResponse.FromString,
            _registered_method=True)
        self.DeleteProduct = channel.unary_unary(
            '/OrderManagementService/DeleteProduct',
            request_serializer=order__management__pb2.OrderOperationRequest.SerializeToString,
            response_deserializer=order__management__pb2.OrderOperationResponse.FromString,
            _registered_method=True)


class OrderManagementServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderManagementServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'AddProduct': grpc.unary_unary_rpc_method_handler(
            servicer.AddProduct,
            request_deserializer=order__management__pb2.OrderOperationRequest.FromString,
            response_serializer=order__management__pb2.OrderOperationResponse.SerializeToString,
        ),
        'DeleteProduct': grpc.unary_unary_rpc_method_handler(
            servicer.DeleteProduct,
            request_deserializer=order__management__pb2.OrderOperationRequest.FromString,
            response_serializer=order__management__pb2.OrderOperationResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'OrderManagementService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers(
        'OrderManagementService', rpc_method_handlers)

 # This class is part of an EXPERIMENTAL API.


class OrderManagementService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddProduct(request,
                   target,
                   options=(),
                   channel_credentials=None,
                   call_credentials=None,
                   insecure=False,
                   compression=None,
                   wait_for_ready=None,
                   timeout=None,
                   metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/OrderManagementService/AddProduct',
            order__management__pb2.OrderOperationRequest.SerializeToString,
            order__management__pb2.OrderOperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteProduct(request,
                      target,
                      options=(),
                      channel_credentials=None,
                      call_credentials=None,
                      insecure=False,
                      compression=None,
                      wait_for_ready=None,
                      timeout=None,
                      metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/OrderManagementService/DeleteProduct',
            order__management__pb2.OrderOperationRequest.SerializeToString,
            order__management__pb2.OrderOperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
