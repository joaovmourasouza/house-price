from datetime import datetime
import pandas as pd
import json
import os

def create_file_name(name: str, type: str):
    """
    A function that creates a file name based on the input name and the current date in the format 'name_dd-mm-yyyy.json'.
    
    Parameters:
    name (str): The base name for the file.
    
    Returns:
    str: The generated file name with the format 'name_dd-mm-yyyy.json'.
    """
    today = datetime.now().strftime('%d-%m-%Y')
    file_name = f'{name}_{today}.{type}'
    return file_name
    
def verify_path(path: str):
    """
    Verify if a given path exists. If it does not exist, create the path.

    Parameters:
        path (str): The path to be verified and created if it does not exist.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def json_file(path: str, name: str, data: dict):
    """
    Generates a JSON file at the specified path with the given data.

    Parameters:
    path (str): The path where the JSON file will be created.
    name (str): The name to be given to the JSON file.
    data (dict): The data to be written into the JSON file.

    Returns:
    str: The full path to the created JSON file.
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    name_file = create_file_name(name=name, type='json')
    folder_path = os.path.join(base_path, 'output', path)
    verify_path(folder_path)
    full_path = os.path.join(folder_path, name_file)
    with open(full_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Arquivo salvo em: {full_path}')
    return full_path

def csv_file(path: str, name: str, dataset: pd.DataFrame):
    """
    Write a pandas DataFrame to a CSV file and return the full path of the created file.

    Args:
        path (str): The subdirectory within the 'output' directory where the CSV file will be saved.
        name (str): The name of the CSV file.
        dataset (pd.DataFrame): The pandas DataFrame to be written to the CSV file.

    Returns:
        str: The full path of the created CSV file.
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    name_file = create_file_name(name=name, type='csv')
    folder_path = os.path.join(base_path, 'output', path)
    verify_path(folder_path)
    full_path = os.path.join(folder_path, name_file)
    dataset.to_csv(full_path, index=False, sep=';', encoding='utf-8')
    return full_path

def merge_datasets():
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    full_path = os.path.join(base_path, 'output','data','silver')
    files_to_load = sorted(os.listdir(full_path))
    dataset = pd.DataFrame()
    for file in files_to_load:
        temp_df = pd.read_csv(os.path.join(full_path, file), sep=';', encoding='utf-8')
        temp_df.columns = [col.lower() for col in temp_df.columns]
        dataset = pd.concat([dataset, temp_df], ignore_index=True)
    dataset = dataset.drop_duplicates(keep='last')
    name_file = create_file_name(name='gold_dataset', type='csv')
    full_path = os.path.join(base_path, 'output','data','gold')
    verify_path(full_path)
    dataset.to_csv(os.path.join(full_path, name_file), index=False, sep=';', encoding='utf-8')