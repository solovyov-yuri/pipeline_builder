import json
import os
import requests


def create_resource(api_url, file_path, ssl_context, logger):
    """
    Creates new resource.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    response = requests.post(api_url, json=data, verify=ssl_context)
    if response.status_code == 200:
        logger.info(f"Created {file_path}: {response.status_code}")
    else:
        logger.warning(f"Error: {response.status_code} {response.text}")


def update_resource(api_url, file_path, ssl_context, logger):
    """
    Updates resource.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    response = requests.put(api_url, json=data, verify=ssl_context)
    if response.status_code == 200:
        logger.info(f"Updated {file_path}: {response.status_code}")
    else:
        logger.warning(f"Error: {response.status_code} {response.text}")


def create_resources(api_url, resources_folder, cert_path, logger):
    """
    Creates requested resources by given api_url.
    """
    ssl_context = cert_path if os.path.exists(cert_path) else False
    folder_path = os.path.join(resources_folder)

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            res_cd = file_name.rstrip(".json")
            file_path = os.path.join(folder_path, file_name)

            response = requests.get(f"{api_url}/{res_cd}", verify=ssl_context)
            if response.status_code == 404:
                create_resource(api_url, file_path, ssl_context, logger)
            elif response.status_code == 200:
                update_resource(f"{api_url}/{res_cd}", file_path, ssl_context, logger)
            else:
                logger.error(f"❌ Error: {response.status_code} {response.text}")
