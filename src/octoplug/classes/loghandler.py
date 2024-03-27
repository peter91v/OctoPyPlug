import logging
import os
import datetime


class LogHandler:
    def __init__(self, log_name, log_dir):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)
        self.log_dir = log_dir
        self.setup_logger(log_name)

    def setup_logger(self, log_name):
        # Erstelle einen Formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Erstelle einen Handler für die Ausgabe in eine Datei
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = os.path.join(
            self.log_dir,
            f"{log_name}_{current_datetime}.log",
        )
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)

        # Füge den Handler zum Logger hinzu
        self.logger.addHandler(file_handler)

        # Erstelle einen StreamHandler für die Ausgabe in die Konsole
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Füge den StreamHandler zum Logger hinzu
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
