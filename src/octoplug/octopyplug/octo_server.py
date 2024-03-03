from concurrent import futures
import json
import logging
import grpc

import octopyplug.octo_pb2 as octo__pb2
import octopyplug.octo_pb2_grpc as octo_pb2__grpc


class MessageService(octo_pb2__grpc.MessageServiceServicer):
    def OctoMessage(self, request, context):
        print("Received message from client:", request.json_message)
        return octo__pb2.OctoResponse(json_message="Message received successfully")

    def GetDataFormat(self, request, context):
        json_format = {
            "": {
                "id": "",
                "text": "",
                "status": 0,
                "grad": 0,
                "class": "",
                "loc": "",
                "datum": "",
                "zeit": "",
                "sid": "",
                "code": 0,
            },
        }

        json_string = json.dumps(json_format)
        return octo__pb2.OctoResponse(json_message=json_string)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    octo_pb2__grpc.add_MessageServiceServicer_to_server(MessageService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started. Listening on port ." + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
