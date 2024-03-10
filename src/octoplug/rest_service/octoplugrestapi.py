import json
import logging
import subprocess
from flask_cors import CORS
from flask import Flask, request, jsonify

# Logger konfigurieren
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

# Flask-App initialisieren
app = Flask(__name__)
CORS(app)

# Funktion zum Lesen der Konfiguration aus einer Datei
def read_config():
    with open("D:\DEV\OctoPyPlug\src\config\config.txt", "r") as file:
        config = json.load(file)
    return config

# Konfiguration lesen
config = read_config()

# Konfigurationswerte für den Python-Interpreter und den Pfad zum Octo-Client abrufen
python_executable = config.get("python_executable", "")
octo_client_path = config.get("octo_client_path", "")

# GET-Endpunkt zum Empfangen von JSON-Daten
@app.route("/", methods=["GET"])
def get_json():
    # Abrufen der Anfrageparameter
    keys = request.args.keys()
    _LOGGER.info("Request keys: %s", keys)
    
    # Zusammenführen aller Anfrageparameter in einem JSON-Objekt
    json_data = {}
    for key in keys:
        json_data[key] = request.args.get(key)
    
    # Überprüfen, ob der Parameter "data" in der Anfrage vorhanden ist
    data = request.args.get("data")
    if data:
        try:
            # Extrahieren der JSON-Daten aus der URL
            json_string = json_data
        except ValueError:
            # Wenn die Daten kein JSON-Format haben, den JSON-String auf die erhaltenen Daten setzen
            json_string = data

        # Externer Prozess mit Python-Ausführungsdatei und JSON-Daten starten
        result = subprocess.run(
            [
                python_executable,
                octo_client_path,
                "5000",
                json.dumps(json_string),  # Daten als JSON-String übergeben
                "SendMessage",
            ],
            stdout=subprocess.PIPE,
        )

        # Daten als JSON-Objekt laden
        try:
            response_data = json.loads(result.stdout)
        except json.JSONDecodeError:
            response_data = result.stdout.decode()  # Fallback, falls die Antwort kein JSON ist

        # Erfolgreiche Antwort mit empfangenen Daten und Statuscode 200 zurückgeben
        return jsonify({"received_data": response_data}), 200
    else:
        # Wenn kein "data"-Parameter angegeben ist, eine Bestätigungsnachricht zurückgeben
        return jsonify({"error": "No JSON data provided in the request"}), 400

# POST-Endpunkt zum Empfangen von JSON-Daten
@app.route("/post_example", methods=["POST"])
def post_example():
    # JSON-Daten aus dem Request-Body abrufen
    data = request.json
    if data:
        try:
            # Externer Prozess mit Python-Ausführungsdatei und JSON-Daten starten
            result = subprocess.run(
                [
                    python_executable,
                    octo_client_path,
                    "5000",
                    json.dumps(data),  # Daten als JSON-String übergeben
                    "SendMessage",
                ],
                stdout=subprocess.PIPE,
            )

            # Daten als JSON-Objekt laden
            try:
                response_data = json.loads(result.stdout)
            except json.JSONDecodeError:
                response_data = result.stdout.decode()  # Fallback, falls die Antwort kein JSON ist

            # Erfolgreiche Antwort mit empfangenen Daten und Statuscode 200 zurückgeben
            return jsonify({"received_data": response_data}), 200
        except:
            # Falls ein Fehler auftritt, eine allgemeine Fehlermeldung zurückgeben
            return jsonify({"error": "An error occurred while processing the request"}), 500
    else:
        # Wenn kein JSON im Request-Body vorhanden ist, eine Fehlermeldung zurückgeben
        return jsonify({"error": "No JSON data provided in the request"}), 400

# Flask-App starten
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=50000)
