import os
import shutil
import time
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from classes.sensorplug import (
    SensorPlug,
)  # Annahme: Klasse, die die 'convert' Methode enthält


# Pfade definieren
input_folder = "D:\DEV\BAC2\Data"
archive_folder = "D:\DEV\BAC2\Data\Archive"


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        # Wenn eine neue Datei erstellt wurde, verarbeite sie
        process_file(event.src_path)


def process_file(file_path):
    # Hier implementieren Sie die Logik zur Verarbeitung der Datei
    # Zum Beispiel: Lesen Sie den Inhalt der Datei, führen Sie Verarbeitungsschritte durch, etc.

    # Datei verarbeiten
    print(f"Verarbeite Datei: {file_path}")

    # Aufrufen der convert-Methode aus der SensorPlug-Klasse
    sensor_plug = SensorPlug()
    converted_data = sensor_plug.convert(file_path)
    print("Konvertierte Daten:", converted_data)

    # Verschieben der Datei in das Archivverzeichnis
    move_to_archive(file_path)


def move_to_archive(file_path):
    # Erstellen Sie den Archivordner mit dem aktuellen Datum als Namen, wenn er noch nicht existiert
    archive_subfolder = os.path.join(
        archive_folder, datetime.now().strftime("%Y-%m-%d")
    )
    if not os.path.exists(archive_subfolder):
        os.makedirs(archive_subfolder)

    # Zeitstempel für Dateinamen generieren
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")

    # Dateiname erstellen
    file_name = os.path.basename(file_path)
    archived_file_name = f"{file_name}_{timestamp}"

    # Zielort für archivierte Datei
    archived_file_path = os.path.join(archive_subfolder, archived_file_name)

    # Verschieben der Datei in das Archivverzeichnis
    shutil.move(file_path, archived_file_path)


if __name__ == "__main__":
    # Überwachung einrichten
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()

    print(f"Überwache das Verzeichnis {input_folder}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
