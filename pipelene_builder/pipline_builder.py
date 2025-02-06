import logging
import os
import re

import paramiko
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def remove_ansi_escape_codes(text):
    """Удаляет ANSI escape-коды из текста."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def copy_files(host, username, ssh_key_path, flow_dir, remote_dir, logger):
    """
    Copy pipeline files to the remote server
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    logger.info(f"Connecting to server: {host}, with user: {username}")
    ssh.connect(host, username=username, key_filename=ssh_key_path)
    logger.info("Connected to the server")

    sftp = ssh.open_sftp()

    for root, _, files in os.walk(flow_dir):
        remote_path = os.path.join(remote_dir, os.path.relpath(root, flow_dir)).replace('\\', '/')

        for file in files:
            if file.startswith("hub_"):
                logger.warning(f"File {file} skipped")
                continue
            local_file = os.path.join(root, file)
            remote_file = os.path.join(remote_path, file).replace('\\', '/')
            sftp.put(local_file, remote_file)
            logger.info(f"File {file} copied to remote server")

    sftp.close()
    ssh.close()
    logger.info("Files copied successfully")


def build_pipeline(host, username, ssh_key_path, dev_env, logger):
    """
    Run the pipeline build on the remote server
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, key_filename=ssh_key_path)

    os.makedirs("logs", exist_ok=True)

    stdin, stdout, stderr = ssh.exec_command(f"sudo bash /app/frm_instances/forcibly_rebuild_dag.sh {dev_env}")

    stdout_text = remove_ansi_escape_codes(stdout.read().decode())
    stderr_text = remove_ansi_escape_codes(stderr.read().decode())

    with open("logs/stderr.log", "w", encoding="utf-8") as log_file:
        log_file.write(stdout_text)

    with open("logs/stdout.log", "w", encoding="utf-8") as log_file:
        log_file.write(stderr_text)

    ssh.close()
    logger.info("Pipeline built successfully, log saved to logs/")
