# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import octopyplug.octo_pb2 as octo__pb2


class MessageServiceStub(object):
    """Definition des Dienstes für Nachrichten"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.OctoMessage = channel.unary_unary(
            "/octo.MessageService/OctoMessage",
            request_serializer=octo__pb2.OctoRequest.SerializeToString,
            response_deserializer=octo__pb2.OctoResponse.FromString,
        )
        self.GetDataFormat = channel.unary_unary(
            "/octo.MessageService/GetDataFormat",
            request_serializer=octo__pb2.GetDataRequest.SerializeToString,
            response_deserializer=octo__pb2.OctoResponse.FromString,
        )


class MessageServiceServicer(object):
    """Definition des Dienstes für Nachrichten"""

    def OctoMessage(self, request, context):
        """Sendet eine Nachricht"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetDataFormat(self, request, context):
        """Ruft das Datenformat ab"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MessageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "OctoMessage": grpc.unary_unary_rpc_method_handler(
            servicer.OctoMessage,
            request_deserializer=octo__pb2.OctoRequest.FromString,
            response_serializer=octo__pb2.OctoResponse.SerializeToString,
        ),
        "GetDataFormat": grpc.unary_unary_rpc_method_handler(
            servicer.GetDataFormat,
            request_deserializer=octo__pb2.GetDataRequest.FromString,
            response_serializer=octo__pb2.OctoResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "octo.MessageService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class MessageService(object):
    """Definition des Dienstes für Nachrichten"""

    @staticmethod
    def OctoMessage(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/octo.MessageService/OctoMessage",
            octo__pb2.OctoRequest.SerializeToString,
            octo__pb2.OctoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetDataFormat(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/octo.MessageService/GetDataFormat",
            octo__pb2.GetDataRequest.SerializeToString,
            octo__pb2.OctoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )