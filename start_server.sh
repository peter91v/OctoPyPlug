#!/bin/bash

# Setze die Ausführungsrechte für das Skript
# chmod +x start_server.sh

# Starte den gRPC-Server
./OctoVenv/Scripts/activate
python ./src/octoplug/octopyplug/octo_server.py --port 5000

