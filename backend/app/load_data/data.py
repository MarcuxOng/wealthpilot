import os
import json

def client_data():
    data_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "client.json")
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file_path}")
        return {"clients": {}}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in data file: {e}")
        return {"clients": {}}
    
def product_data():
    data_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "products.json")
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file_path}")
        return {"products": {}}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in data file: {e}")
        return {"products": {}}

client_data = client_data()
product_data = product_data()