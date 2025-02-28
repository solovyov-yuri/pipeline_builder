import sys

from src.config import config
from src.db_entities_creator import create_gp_entities, create_oracle_entities
from src.logger import LoggerConfig
from src.pipline_builder import build_pipeline_with_progress, copy_files
from src.resource_creator import create_resources

# Setup logger
logger = LoggerConfig.get_logger("Pipeline Builder")

# Load configuration
# Development environment
dev_env = sys.argv[1] if len(sys.argv) > 1 else "develop"

# Database connection settings
gp_config = config.get(f"database.greenplum.{dev_env}")
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
ddl_dir = config.get("directories.local.ddl")

ssl_cert_path = config.get("ssl.cert_path")


def main():
    """Main logic"""
    logger.info("Builder start working...")

    # Copiy files to remote server
    copy_files(server_conn, flow_dir, remote_dir, logger)

    # Create UNI resources
    create_resources(uni_res_url, uni_res_dir, logger, ssl_cert_path)

    # # Create CEH resources
    create_resources(ceh_res_url, ceh_res_dir, logger, ssl_cert_path)

    # Create tables in database
    create_gp_entities(ddl_dir, gp_config, logger)
    create_oracle_entities(ddl_dir, oracle_config, logger)

    # Start remote build via ssh
    build_pipeline_with_progress(server_conn, dev_env, logger)


if __name__ == "__main__":
    main()
