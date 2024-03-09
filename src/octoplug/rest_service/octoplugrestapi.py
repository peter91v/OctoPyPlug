import json
import flask

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_json', methods=['GET'])
def get_json():
    data = request.args.get('data')  # JSON-Daten aus der URL abrufen
    try:
        json_data = json.loads(data)  # JSON-Daten parsen
        # Hier können Sie die empfangenen Daten verarbeiten
        return jsonify({'received_data': json_data}), 200
    except json.JSONDecodeError as e:
        return jsonify({'error': 'Invalid JSON format'}), 400


@app.route('/post_example', methods=['POST'])
def post_example():
    # Hier können Sie den POST-Request verarbeiten
    data = request.json  # JSON-Daten aus dem Request-Body abrufen
    # Verarbeiten Sie die Daten hier
    return jsonify({'message': 'Data received successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
