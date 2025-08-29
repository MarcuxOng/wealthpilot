import os
import json

def load_data():
    data_file_path = os.path.join(os.path.dirname(__file__), "data.json")
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file_path}")
        return {"clients": {}, "products": {}}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in data file: {e}")
        return {"clients": {}, "products": {}}

db_data = load_data()
