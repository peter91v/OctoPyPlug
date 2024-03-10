import json  # Bibliothek zum Arbeiten mit JSON-Daten
import subprocess  # Bibliothek zum Ausführen von externen Prozessen
import flask  # Framework für Webanwendungen
import os  # Bibliothek zum Arbeiten mit dem Dateisystem
from flask_cors import CORS  # Bibliothek für Cross-Origin Resource Sharing

from flask import Flask, request, jsonify  # Import von Flask-Modulen

app = Flask(__name__)  # Erstellen einer Flask-App
CORS(app)  # Aktivieren von Cross-Origin Resource Sharing für die App


def read_config():
    """
    Funktion zum Lesen der Konfiguration aus einer Datei.

    Returns:
        dict: Das gelesene Konfigurationsobjekt.
    """
    with open("D:\DEV\BAC2\src\config\config.txt", "r") as file:
        config = json.load(file)
    return config


config = read_config()  # Lesen der Konfiguration aus der Datei

# Extrahieren der Python-Ausführungsdatei und des Pfads zum Octo-Client
python_executable = config.get("python_executable", "")
octo_client_path = config.get("octo_client_path", "")


@app.route("/", methods=["GET"])
def get_json():
    """
    Endpunkt zum Empfangen von JSON-Daten über GET-Anfragen.

    Returns:
        tuple: HTTP-Antwort mit empfangenen Daten und Statuscode.
    """
    data = request.args.get("data")  # JSON-Daten aus der URL abrufen
    try:
        json_string = jsonify(data).get_data(as_text=True)
        # Externen Prozess mit Python-Ausführungsdatei und JSON-Daten starten
        result = subprocess.run(
            [
                python_executable,
                octo_client_path,
                "5000",
                json_string,
                "SendMessage",
            ],
            stdout=subprocess.PIPE,
        )
        # Daten als JSON-Objekt laden
        data = json.loads(data)
        # Erfolgreiche Antwort mit empfangenen Daten und Statuscode 200 zurückgeben
        return jsonify({"received_data": data}), 200
    except json.JSONDecodeError as e:
        # Fehlerantwort bei ungültigem JSON-Format und Statuscode 400 zurückgeben
        return jsonify({"error": "Invalid JSON format"}), 400


@app.route("/post_example", methods=["POST"])
def post_example():
    """
    Endpunkt zum Empfangen von JSON-Daten über POST-Anfragen.

    Returns:
        tuple: HTTP-Antwort mit empfangenen Daten und Statuscode.
    """
    data = request.json  # JSON-Daten aus dem Request-Body abrufen
    try:
        json_string = jsonify(data).get_data(as_text=True)
        # Externen Prozess mit Python-Ausführungsdatei und JSON-Daten starten
        result = subprocess.run(
            [
                python_executable,
                octo_client_path,
                json_string,
                "SendMessage",
            ],
            stdout=subprocess.PIPE,
        )
        # Erfolgreiche Antwort mit empfangenen Daten und Statuscode 200 zurückgeben
        return jsonify({"received_data": data}), 200
    except json.JSONDecodeError as e:
        # Fehlerantwort bei ungültigem JSON-Format und Statuscode 400 zurückgeben
        return jsonify({"error": "Invalid JSON format"}), 400
    # Verarbeitung der Daten und Antwort mit Statuscode 200 zurückgeben
    return jsonify({"message": "Data received successfully"}), 200


if __name__ == "__main__":
    # Starten der Flask-App auf dem Server mit Host "0.0.0.0" und Port 50000
    app.run(host="0.0.0.0", port=50000)
