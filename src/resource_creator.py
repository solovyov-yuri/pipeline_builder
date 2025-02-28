import json
import os
from logging import Logger

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout


def find_resources(resource_dir: str) -> list:
    resources = []

    for root, _, files in os.walk(resource_dir):
        for file in files:
            if file.endswith(".json"):
                res_cd = file.rstrip(".json")
                resources.append({"res_cd": res_cd, "res_path": os.path.join(root, file)})

    return resources


def load_json(file_path: str, logger: Logger) -> dict:
    """
    Load JSON file from given path.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"❌ Error loading JSON from {file_path}: {e}")
        return None


def create_resource(api_url: str, res_cd: str, file_path: str, ssl_context: str, logger: Logger) -> None:
    """
    Creates new resource.
    """
    data = load_json(file_path, logger)
    if data is None:
        return

    try:
        response = requests.post(f"{api_url}", json=data, verify=ssl_context)
        if response.status_code == 200:
            logger.info(f"✅ Resource {res_cd} created.")
        else:
            logger.warning(f"❌ Error creating {res_cd}: {response.status_code} {response.text}")

    except (ConnectionError, HTTPError, Timeout, RequestException) as e:
        logger.error(f"🛑 Error creating resource {res_cd}: {e}")
    except Exception as e:
        logger.error(f"❌ Error: {e}")


def update_resource(api_url: str, res_cd: str, file_path: str, ssl_context: str, logger: Logger) -> None:
    """
    Updates resource.
    """
    data = load_json(file_path, logger)
    if data is None:
        return

    try:
        response = requests.put(f"{api_url}/{res_cd}", json=data, verify=ssl_context)
        if response.status_code == 200:
            logger.info(f"✅ Resource {res_cd} updated.")
        else:
            logger.warning(f"❌ Error updating {res_cd}: {response.status_code} {response.text}")

    except (ConnectionError, HTTPError, Timeout, RequestException) as e:
        logger.error(f"❌ Error creating resource {res_cd}: {e}")
    except Exception as e:
        logger.error(f"❌ Error: {e}")


def reset_resource(api_url: str, res_cd: str, logger: Logger, ssl_context: str) -> None:
    """
    Resets resource.
    """
    try:
        response = requests.put(f"{api_url}/{res_cd}/reset", verify=ssl_context)
        if response.status_code == 200:
            logger.info(f"✅ Resource {res_cd} reset.")
        else:
            logger.warning(f"❌ Error resetting {res_cd}: {response.status_code} {response.text}")

    except (ConnectionError, HTTPError, Timeout, RequestException) as e:
        logger.error(f"❌ Error creating resource {res_cd}: {e}")
    except Exception as e:
        logger.error(f"❌ Error: {e}")


def create_resources(api_url: str, resources_dir: str, logger: Logger, cert_path: str = "") -> None:
    """
    Creates requested resources by given api_url.
    """
    print(api_url, resources_dir)
    ssl_context = cert_path if os.path.exists(cert_path) else False

    resources = find_resources(resources_dir)
    logger.info(f"ℹ️ Found resources {resources}")

    for res in resources:
        res_cd = res["res_cd"]
        res_path = res["res_path"]
        try:
            response = requests.get(f"{api_url}/{res_cd}", verify=ssl_context)
        except ConnectionError as e:
            logger.error(f"❌ Connection error: {e}. Ensure your VPN is on and the resource provider url is correct.")

        if response.status_code == 404:
            create_resource(api_url, res_cd, res_path, ssl_context, logger)
        elif response.status_code == 200:
            update_resource(api_url, res_cd, res_path, ssl_context, logger)
            reset_resource(api_url, res_cd, logger, ssl_context)
        else:
            logger.error(f"❌ Error: {response.status_code} {response.text}")
