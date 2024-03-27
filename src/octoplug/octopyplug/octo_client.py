import argparse
from datetime import datetime, timedelta
import os
import grpc
import json
from typing import Any

import _credentials
import octopyplug.octo_pb2 as octo_pb2
import octopyplug.octo_pb2_grpc as octo_pb2_grpc
import classes.sensorplug as Sensorplug

# Importiere die LogHandler-Klasse
from classes.loghandler import LogHandler

# Erhalte den Logger von LogHandler
log_handler = LogHandler(os.path.basename(__file__)[:-3], "D:\\DEV\\BAC2\\Log")
logger = log_handler.get_logger()

# Vorlage für die Serveradresse
_SERVER_ADDR_TEMPLATE = "localhost:%d"

# Typen von Clientanfragen
_CLIENT_REQUEST_TYPES = ["SendMessage", "GetFormat"]


def create_client_channel(addr: str) -> grpc.Channel:
    """
    Funktion zum Erstellen eines gRPC-Clientkanals.

    Args:
        addr (str): Die Adresse des Servers.

    Returns:
        grpc.Channel: Der erstellte gRPC-Clientkanal.
    """
    # Zugriffstoken-Credentials für jede RPC-Anfrage
    call_credentials = grpc.access_token_call_credentials("test_token")
    # SSL-Credentials für den gesamten Kanal
    channel_credential = grpc.ssl_channel_credentials(_credentials.ROOT_CERTIFICATE)
    # Kombinierte Credentials für den Kanal
    composite_credentials = grpc.composite_channel_credentials(
        channel_credential,
        call_credentials,
    )
    # Erstellen und Rückgabe des sicheren Kanals
    channel = grpc.secure_channel(addr, composite_credentials)
    return channel


def is_file_recent(file_path, days=5):
    """
    Überprüft, ob die Datei vorhanden und nicht älter als die angegebene Anzahl von Tagen ist.

    Args:
        file_path (str): Der Pfad zur zu überprüfenden Datei.
        days (int): Die maximale Anzahl von Tagen, die die Datei zurückliegen darf. Standardmäßig 5 Tage.

    Returns:
        bool: True, wenn die Datei vorhanden und nicht älter als die angegebene Anzahl von Tagen ist, False sonst.
    """
    if not os.path.exists(file_path):
        return False
    file_time = os.path.getmtime(file_path)
    current_time = datetime.now().timestamp()
    age_in_days = (current_time - file_time) / (60 * 60 * 24)
    return age_in_days <= days


def run(channel: grpc.Channel, json_message: Any, type: str) -> Any:
    """
    Funktion zum Ausführen einer RPC-Anfrage an den Server.

    Args:
        channel (grpc.Channel): Der gRPC-Clientkanal.
        json_message (Any): Die JSON-Daten der Anfrage.
        type (str): Der Typ der Anfrage.

    Returns:
        Any: Die Antwort des Servers.
    """
    stub = octo_pb2_grpc.MessageServiceStub(channel)
    try:
        json_string = json.dumps(json_message)
        if type == _CLIENT_REQUEST_TYPES[0]:
            # Senden der Anfrage zum Senden einer Nachricht
            response = stub.OctoMessage(octo_pb2.OctoRequest(json_message=json_string))
        elif type == _CLIENT_REQUEST_TYPES[1]:
            if not is_file_recent("dataschema.json"):
                # Datei ist nicht vorhanden oder älter als 5 Tage, rufen Sie den Server mit GetFormat auf
                response = stub.GetDataFormat(octo_pb2.OctoRequest())
                # Speichern Sie das empfangene Datenformat in dataschema.json
                with open("dataschema.json", "w") as file:
                    file.write(response.json_message)
            else:
                # Verwenden Sie die vorhandene dataschema.json-Datei
                with open("dataschema.json", "r") as file:
                    response = octo_pb2.OctoResponse(json_message=file.read())
        else:
            response = None
    except grpc.RpcError as rpc_error:
        logger.error("Received error: %s", rpc_error)
        return rpc_error
    else:
        logger.info("Received message: %s", response)
        return response


def main():
    """
    Hauptfunktion des Programms.
    """
    # Parsen der Befehlszeilenargumente
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, default=5000, help="the port of server")
    parser.add_argument("json_message", default="", help="JSON message to send")
    parser.add_argument(
        "type",
        choices=_CLIENT_REQUEST_TYPES,
        default=_CLIENT_REQUEST_TYPES[0],
        help="Type of request",
    )
    args = parser.parse_args()

    with create_client_channel(_SERVER_ADDR_TEMPLATE % args.port) as channel:
        # Ausführen der RPC-Anfrage
        data = Sensorplug.SensorPlug.convert(args.json_message)
        response = run(channel, data, args.type)

    # Drucken der Antwort
    print(response)


if __name__ == "__main__":
    main()
