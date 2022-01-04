import json

def read_json(file_path):
    """This function read json files
    """
    with open(file_path, 'r') as f:
        return json.load(f)