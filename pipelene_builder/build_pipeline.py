import logging
import os
import sys

from db_entities_creator import (create_or_update_entities,
                                 create_oracle_entities)
from pipline_builder import build_pipeline, copy_files
from resource_creator import create_ceh_resources, create_uni_resources

# Configuration
DEV_ENVIRONMENTS = {
    "zi5": {
        "dir": os.getenv("ZI5_DIR"),
        "uni_res_prov": os.getenv("ZI5_UNI_RESOURCE_PROVIDER"),
        "ceh_res_prov": os.getenv("ZI5_CEH_RESOURCE_PROVIDER"),
        "gp_config": {
            "dbname": os.getenv("ZI5_GP_DB"),
            "user": os.getenv("ZI5_GP_USER"),
            "password": os.getenv("ZI5_GP_PASS"),
            "host": os.getenv("ZI5_GP_HOST"),
            "port": os.getenv("ZI5_GP_PORT")
        }
    },
    "develop": {
        "dir": os.getenv("DEVELOP_DIR"),
        "uni_res_prov": os.getenv("DEVELOP_UNI_RESOURCE_PROVIDER"),
        "ceh_res_prov": os.getenv("DEVELOP_CEH_RESOURCE_PROVIDER"),
        "gp_config": {
            "dbname": os.getenv("DEVELOP_GP_DB"),
            "user": os.getenv("DEVELOP_GP_USER"),
            "password": os.getenv("DEVELOP_GP_PASS"),
            "host": os.getenv("DEVELOP_GP_HOST"),
            "port": os.getenv("DEVELOP_GP_PORT")
        }
    }
}

# Development environment
DEV_ENV = sys.argv[1] if len(sys.argv) > 1 else "develop"

if DEV_ENV not in DEV_ENVIRONMENTS:
    print(f"❌ Unknown environment: {DEV_ENV}. Available: {list(DEV_ENVIRONMENTS.keys())}")
    sys.exit(1)

# Server connection
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PORT = os.getenv("PORT")
SSH_KEY_PATH = os.getenv("SSH_KEY_PATH")

# Directories
FLOW_DIR = f"{os.getcwd()}/src_rdv"
REMOTE_DIR = DEV_ENVIRONMENTS[DEV_ENV]["dir"]
DDL_DIR = os.getenv("DDL_DIR")

CERT_PATH = os.getenv("CERT_PATH")

# Database connection settings
ORACLE_CONFIG = {
    "user": os.getenv("DEV_ORACLE_USER"),
    "password": os.getenv("DEV_ORACLE_PASS"),
    "dsn": f"{os.getenv('DEV_ORACLE_HOST')}:{os.getenv('DEV_ORACLE_PORT')}/{os.getenv('DEV_ORACLE_SERVICE_NAME')}"
}
GP_CONFIG = DEV_ENVIRONMENTS[DEV_ENV]["gp_config"]

# Resource providers
UNI_RES = DEV_ENVIRONMENTS[DEV_ENV].get("uni_res_prov", "")
CEH_RES = DEV_ENVIRONMENTS[DEV_ENV].get("ceh_res_prov", "")


def setup_logging():
    """Configure logging"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def validate_env(logger):
    """Check environment variables"""
    required_vars = ["HOST", "USER", "PORT", "SSH_KEY_PATH", "CERT_PATH"]
    required_db_vars = [
        "DEV_ORACLE_USER", "DEV_ORACLE_PASS", "DEV_ORACLE_HOST",
        "DEV_ORACLE_PORT", "DEV_ORACLE_SERVICE_NAME",
        "DEV_GP_DB", "DEV_GP_USER", "DEV_GP_PASS", "DEV_GP_DB_HOST", "DEV_GP_PORT"
    ]

    for var in required_vars + required_db_vars:
        if not os.getenv(var):
            logger.error(f"❌ Environment variable {var} is not set!")
            sys.exit(1)


def main():
    """Main logic"""
    global logger
    logger.info("Builder start working...")

    copy_files(HOST, USER, SSH_KEY_PATH, FLOW_DIR, REMOTE_DIR, logger)

    if UNI_RES:
        create_uni_resources(api_url=UNI_RES, resources_folder='_resources', cert_path=CERT_PATH, logger=logger)
    else:
        logger.warning("⚠️ UNI_RES is not set! Skipping resource creation.")

    if CEH_RES:
        create_ceh_resources(api_url=CEH_RES, resources_folder='_resources', cert_path=CERT_PATH, logger=logger)
    else:
        logger.warning("⚠️ CEH_RES is not set! Skipping resource creation.")

    create_or_update_entities(DDL_DIR, GP_CONFIG, logger)
    create_oracle_entities(DDL_DIR, ORACLE_CONFIG, logger)

    build_pipeline(HOST, USER, SSH_KEY_PATH, DEV_ENV, logger)


if __name__ == "__main__":
    logger = setup_logging()
    validate_env(logger)
    main()
