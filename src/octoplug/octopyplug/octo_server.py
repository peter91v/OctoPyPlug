import argparse
from concurrent import futures
import contextlib
import logging
import json

import grpc

import _credentials  # Import von benutzerdefinierten Anmeldeinformationen
import octopyplug.octo_pb2 as octo_pb2  # Import der generierten Protokollklassen
import octopyplug.octo_pb2_grpc as octo_pb2_grpc  # Import der generierten gRPC-Services

# Konfigurieren des Loggers
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

# Vorlage für die Serveradresse
_LISTEN_ADDRESS_TEMPLATE = "localhost:%d"
# Schlüssel und Wert für die Authentifizierung
_AUTH_HEADER_KEY = "authorization"
_AUTH_HEADER_VALUE = "Bearer test_token"


class SignatureValidationInterceptor(grpc.ServerInterceptor):
    """
    Serverinterceptor zur Signaturvalidierung.
    """

    def __init__(self):
        """
        Initialisierungsmethode für den Interceptor.
        """

        # Handler für ungültige Signatur
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid signature")

        # Handler-Methode
        self._abort_handler = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        """
        Interceptor-Methode zum Abfangen des Dienstaufrufs.

        Args:
            continuation: Fortsetzungsfunktion für die Dienstverarbeitung.
            handler_call_details: Details des Dienstaufrufs.

        Returns:
            continuation: Fortsetzung der Dienstverarbeitung oder Abbruchhandler.
        """
        # Erwartete Metadaten für die Authentifizierung
        expected_metadata = (_AUTH_HEADER_KEY, _AUTH_HEADER_VALUE)
        if expected_metadata in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._abort_handler


class MessageService(octo_pb2_grpc.MessageServiceServicer):
    """
    Implementation des gRPC-Services für die Nachrichtenverarbeitung.
    """

    def OctoMessage(self, request, context):
        """
        Methode zum Empfangen einer Octo-Nachricht.

        Args:
            request: Anforderungsnachricht.
            context: Kontext des Dienstaufrufs.

        Returns:
            OctoResponse: Antwortnachricht.
        """
        json_message = json.loads(request.json_message)
        _LOGGER.info("Received message from client: %s", json_message)
        return octo_pb2.OctoResponse(json_message="Message received successfully")

    def GetDataFormat(self, request, context):
        """
        Methode zum Abrufen des Datenformats.

        Args:
            request: Anforderungsnachricht.
            context: Kontext des Dienstaufrufs.

        Returns:
            OctoResponse: Antwortnachricht.
        """
        json_format = {
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
        }

        json_string = json.dumps(json_format)
        return octo_pb2.OctoResponse(json_message=json_string)


@contextlib.contextmanager
def run_server(port):
    """
    Funktion zum Ausführen des gRPC-Servers.

    Args:
        port (int): Der Port, auf dem der Server lauscht.

    Yields:
        tuple: Tupel mit dem Serverobjekt und dem Port.
    """
    # Erstellen des gRPC-Servers mit Interceptor
    server = grpc.server(
        futures.ThreadPoolExecutor(),
        interceptors=(SignatureValidationInterceptor(),),
    )
    # Hinzufügen des Dienstes zum Server
    octo_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(), server)

    # Laden der Serverzertifikate
    server_credentials = grpc.ssl_server_credentials(
        ((_credentials.SERVER_CERTIFICATE_KEY, _credentials.SERVER_CERTIFICATE),)
    )

    # Hinzufügen des sicheren Ports zum Server
    port = server.add_secure_port(_LISTEN_ADDRESS_TEMPLATE % port, server_credentials)

    # Starten des Servers und Rückgabe von Server und Port
    server.start()
    try:
        yield server, port
    finally:
        server.stop(0)


def main():
    """
    Hauptfunktion des Programms.
    """
    # Parsen der Befehlszeilenargumente
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", nargs="?", type=int, default=5000, help="the listening port"
    )
    args = parser.parse_args()

    # Ausführen des Servers
    with run_server(args.port) as (server, port):
        _LOGGER.info("Server is listening at port :%d", port)
        # Auf das Beenden des Servers warten
        server.wait_for_termination()


if __name__ == "__main__":
    # Konfigurieren des Loggers und Starten des Hauptprogramms
    logging.basicConfig(level=logging.INFO)
    main()
