import json
import os

class FileIO:
    @staticmethod
    def read_json(file_path):
        """Read JSON data with proper error handling"""
        try:
            if not os.path.exists(file_path):
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Error reading JSON file: {e}")
            # Try to recover by creating a new file
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except (IOError, OSError):
                pass
            return []

    @staticmethod
    def write_json(file_path, data):
        """Write JSON data with proper error handling"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write to temporary file first for safety
            temp_path = file_path + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Atomically replace the original file
            os.replace(temp_path, file_path)
            return True
        except (IOError, OSError, TypeError, ValueError) as e:
            print(f"Error writing JSON file: {e}")
            # Clean up temp file if it exists
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except (IOError, OSError):
                pass
            return False