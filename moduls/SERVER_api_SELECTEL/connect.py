import json
import os

class SelectelServerConnector:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(current_dir, 'config.json')

    def load_configuration(self) -> dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"server_url": "localhost", "environment": "development"}
