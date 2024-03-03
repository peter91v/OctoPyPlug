from flask import Flask, request
from configparser import ConfigParser
import requests
import json
import urllib
import hashlib

users = {"kunal": "1234", "user2": "password2", "John": "New York"}


class RestService:

    def __init__(self, name=__name__):
        self.app = Flask(name)
        self.config = None
        self.load_config()
        self.setup_routes()
        self.description = None  # description initialisieren
        self.hash_token = None

    def load_config(self):
        self.config = ConfigParser()
        self.config.read("data/config.ini")
        self.app.config["DEBUG"] = self.config.getboolean("Flask", "DEBUG")
        self.app.config["SECRET_KEY"] = self.config.get("Flask", "SECRET_KEY")
        self.hash_token = self.config.get("Security", "HASH_TOKEN")

    def fetch_description(self):
        if request.method == "GET":
            json_data = request.args.get("data")
            decoded_data = self.decode_with_token(json_data)
            data = json.loads(decoded_data)
            username = data.get("username")
            password = data.get("password")

            print(username, password, json_data)
            if username in users and users[username] == password:
                return "<h1>Welcome!!!</h1>"
            else:
                return "<h1>invalid credentials!</h1>"
        else:
            return self.description

    def encode_with_token(self, data):
        encoded_data = hashlib.sha256((data + self.hash_token).encode()).hexdigest()
        return encoded_data

    # Funktion zum Decodieren mit dem Hash-Token
    def decode_with_token(self, encoded_data):
        decoded_data = encoded_data[: -len(self.hash_token)]
        return decoded_data

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return "Hallo"

        @self.app.route("/data", methods=["GET"])
        def data():
            return str(
                self.fetch_description()
            )  # Hier fetch_description() mit Klammern aufrufen

        @self.app.route("/about")
        def about():
            return "About Page"

    def run(self):
        self.app.run(
            host=self.config.get("Network", "IP"),
            port=self.config.getint("Network", "Port"),  # Port sollte ein Integer sein
        )
