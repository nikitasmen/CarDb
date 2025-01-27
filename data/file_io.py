import json
import os

class FileIO:
    @staticmethod
    def read_json(file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)