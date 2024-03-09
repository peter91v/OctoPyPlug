import json
import subprocess
import flask
import os
from flask_cors import CORS

from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)


def read_config():
    with open("D:\DEV\BAC2\src\config\config.txt", "r") as file:
        config = json.load(file)
    return config


config = read_config()

python_executable = config.get("python_executable", "")
octo_client_path = config.get("octo_client_path", "")


@app.route("/", methods=["GET"])
def get_json():
    data = request.args.get("data")  # JSON-Daten aus der URL abrufen
    try:
        json_string = jsonify(data).get_data(as_text=True)
        result = subprocess.run(
            [
                python_executable,
                octo_client_path,
                json_string,
                "SendMessage",
            ],
            stdout=subprocess.PIPE,
        )
        # return result.stdout

        return jsonify({"received_data": data}), 200
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON format"}), 400


@app.route("/post_example", methods=["POST"])
def post_example():
    # Hier können Sie den POST-Request verarbeiten
    data = request.json  # JSON-Daten aus dem Request-Body abrufen
    try:
        json_string = jsonify(data).get_data(as_text=True)
        result = subprocess.run(
            [
                python_executable,
                octo_client_path,
                json_string,
                "SendMessage",
            ],
            stdout=subprocess.PIPE,
        )
        # return result.stdout

        return jsonify({"received_data": data}), 200
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON format"}), 400
    # Verarbeiten Sie die Daten hier
    return jsonify({"message": "Data received successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
