from logger import LoggerConfig
import os
import sys

from config import config

# from db_entities_creator import create_or_update_entities, create_oracle_entities
# from pipline_builder import build_pipeline, copy_files, get_files_from_dir
from resource_creator import create_resources


logger = LoggerConfig.get_logger("Pipeline Builder")

# Load configuration
# Development environment
dev_env = sys.argv[1] if len(sys.argv) > 1 else "develop"

# Database connection settings
gp_config = config.get("database.greenplum")
oracle_config = config.get("database.oracle")

# Resource providers api's
uni_res_url = config.get(f"resource_provider.{dev_env}.uni_res")
ceh_res_url = config.get(f"resource_provider.{dev_env}.ceh_res")

# Server connection
server_conn = config.get("server")

# Directories
flow_dir = config.get("directories.local.flow")
remote_dir = config.get("directories.remote")[dev_env]
uni_res_dir = config.get("directories.local.uni_res")
ceh_res_dir = config.get("directories.local.ceh_res")

ssl_cert_path = config.get("ssl.cert_path")

# DEV_ENVIRONMENTS = {
#     "zi5": {
#         "dir": os.getenv("ZI5_DIR"),
#         "uni_res_prov": os.getenv("ZI5_UNI_RESOURCE_PROVIDER"),
#         "ceh_res_prov": os.getenv("ZI5_CEH_RESOURCE_PROVIDER"),
#         "gp_config": {
#             "dbname": os.getenv("ZI5_GP_DB"),
#             "user": os.getenv("ZI5_GP_USER"),
#             "password": os.getenv("ZI5_GP_PASS"),
#             "host": os.getenv("ZI5_GP_HOST"),
#             "port": os.getenv("ZI5_GP_PORT"),
#         },
#     },
#     "develop": {
#         "dir": os.getenv("DEVELOP_DIR"),
#         "uni_res_prov": os.getenv("DEVELOP_UNI_RESOURCE_PROVIDER"),
#         "ceh_res_prov": os.getenv("DEVELOP_CEH_RESOURCE_PROVIDER"),
#         "gp_config": {
#             "dbname": os.getenv("DEVELOP_GP_DB"),
#             "user": os.getenv("DEVELOP_GP_USER"),
#             "password": os.getenv("DEVELOP_GP_PASS"),
#             "host": os.getenv("DEVELOP_GP_HOST"),
#             "port": os.getenv("DEVELOP_GP_PORT"),
#         },
#     },
# }

# # Development environment
# DEV_ENV = sys.argv[1] if len(sys.argv) > 1 else "develop"

# # Server connection
# HOST = os.getenv("HOST")
# USER = os.getenv("USER")
# PORT = os.getenv("PORT")
# SSH_KEY_PATH = os.getenv("SSH_KEY_PATH")
# SERVER_PASS = os.getenv("SERVER_PASS")

# # Directories
# REMOTE_DIR = DEV_ENVIRONMENTS[DEV_ENV]["dir"]
# DDL_DIR = os.getenv("DDL_DIR")
# UNI_RES_DIR = os.getenv("UNI_RES_DIR")
# CEH_RES_DIR = os.getenv("CEH_RES_DIR")

# CERT_PATH = os.getenv("CERT_PATH")

# # Database connection settings
# ORACLE_CONFIG = {
#     "user": os.getenv("DEV_ORACLE_USER"),
#     "password": os.getenv("DEV_ORACLE_PASS"),
#     "dsn": f"{os.getenv('DEV_ORACLE_HOST')}:{os.getenv('DEV_ORACLE_PORT')}/{os.getenv('DEV_ORACLE_SERVICE_NAME')}",
# }
# GP_CONFIG = DEV_ENVIRONMENTS[DEV_ENV]["gp_config"]

# # Resource providers
# UNI_RES = DEV_ENVIRONMENTS[DEV_ENV].get("uni_res_prov", "")
# CEH_RES = DEV_ENVIRONMENTS[DEV_ENV].get("ceh_res_prov", "")


# def validate_env(logger):
#     """Check environment variables"""
#     required_vars = ["HOST", "USER", "PORT", "SSH_KEY_PATH", "CERT_PATH"]
#     required_dirs = ["DDL_DIR", "UNI_RES_DIR", "CEH_RES_DIR"]
#     required_db_configs = []

#     for var in required_vars + required_dirs + required_db_configs:
#         if not os.getenv(var):config.example.yamlconfig.example.yaml
#             logger.warning(f"⚠️ Environment variable {var} is not set!")


def main():
    """Main logic"""
    logger.info("Builder start working...")

    # Copiy files to remote server
    # copy_files(server_conn, flow_dir, remote_dir, logger)

    # Create UNI resources
    create_resources(uni_res_url, uni_res_dir, logger, ssl_cert_path)

    # # Create CEH resources
    create_resources(ceh_res_url, ceh_res_dir, logger, ssl_cert_path)

    # # Create tables in database
    # create_or_update_entities(DDL_DIR, GP_CONFIG, logger)
    # create_oracle_entities(DDL_DIR, ORACLE_CONFIG, logger)

    # # Start remote build via ssh
    # build_pipeline(HOST, USER, SERVER_PASS, DEV_ENV, logger)


if __name__ == "__main__":
    # validate_env(logger)
    main()
