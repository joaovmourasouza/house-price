import json
import os

def json_file(path: str):
    """
    Load data from a JSON file located at the specified path.

    Parameters:
    path (str): The path to the JSON file.

    Returns:
    dict: The data loaded from the JSON file.
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(base_path, path), 'r') as file:
        data = json.load(file)
    return data