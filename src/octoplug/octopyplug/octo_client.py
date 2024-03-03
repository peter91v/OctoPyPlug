# -*- coding: utf-8 -*-
import grpc
import logging
import octopyplug.octo_pb2 as octo__pb2
import octopyplug.octo_pb2_grpc as octo_pb2__grpc

import sys
import json

ClientRequestTyp = ["SendMessage", "GetFormat"]


def run(json_message, type):
    channel = grpc.insecure_channel("localhost:50051")
    stub = octo_pb2__grpc.MessageServiceStub(channel)
    # Convert JSON message to string

    json_string = json.dumps(json_message)
    if type == ClientRequestTyp[0]:
        response = stub.OctoMessage(octo__pb2.OctoRequest(json_message=json_string))
    # print("Response from server:", response.json_message)
    elif type == ClientRequestTyp[1]:
        response = stub.GetDataFormat(octo__pb2.OctoRequest())
    # print("Response from server (GetDataFormat):", response.json_message)
    else:
        response = None
    return response.json_message


if __name__ == "__main__":
    logging.basicConfig()
    if len(sys.argv) != 3:
        print("Usage: python client.py <json_message>")
        sys.exit(1)
    json_message = json.loads(sys.argv[1])
    test = run(json_message, (sys.argv[2]))
    print(test.json_message)
