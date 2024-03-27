import argparse
import json
import logging
import os
import subprocess
from flask_cors import CORS
from flask import Flask, request, jsonify

# Importiere die LogHandler-Klasse
from classes.loghandler import LogHandler

# Erhalte den Logger von LogHandler
app = Flask(__name__)
CORS(app)
log_handler = LogHandler(app.name, "D:\\DEV\\BAC2\\Log")
LOGGER = log_handler.get_logger()


CONFIG_PATH = "D:\DEV\BAC2\src\config\config.txt"
config = {}


def load_config():
    global config
    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)


load_config()


def run_subprocess(json_string: str):
    python_executable = config.get("python_executable", "")
    octo_client_path = config.get("octo_client_path", "")
    result = subprocess.run(
        [python_executable, octo_client_path, "5000", json_string, "SendMessage"],
        stdout=subprocess.PIPE,
    )
    return result.stdout


@app.route("/", methods=["GET"])
def get_json():
    keys = request.args.keys()
    LOGGER.info("Request keys: %s", keys)
    params_json = {key: request.args.get(key) for key in keys}
    data = params_json.get("data")

    if data:
        try:
            params_json = json.loads(data)
            json_string = json.dumps(params_json)
        except ValueError:
            json_string = data

        result = run_subprocess(json_string)

        try:
            response_data = json.loads(result)
        except json.JSONDecodeError:
            response_data = result.decode().replace("\r", "").replace("\n", "")
        return jsonify({"received_data": response_data}), 200

    return jsonify({"error": "No JSON data provided in the request"}), 400


@app.route("/post_example", methods=["POST"])
def post_example():
    data = request.json

    if data:
        try:
            json_string = json.dumps(data)
            result = run_subprocess(json_string)
            try:
                response_data = json.loads(result)
            except json.JSONDecodeError:
                response_data = result.decode()
            return jsonify({"received_data": response_data}), 200
        except:
            return (
                jsonify({"error": "An error occurred while processing the request"}),
                500,
            )

    return jsonify({"error": "No JSON data provided in the request"}), 400


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="the host of server"
    )
    parser.add_argument("--port", type=int, default=50000, help="the port of server")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    host = args.host
    port = args.port
    app.run(host, port)
    LOGGER.info("RestApi wurde an Host: {host} mit Port: {port} gestartet.")
