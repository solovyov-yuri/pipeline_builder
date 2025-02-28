import os
import re
import sys
import threading
import time
from logging import Logger
from socket import gaierror

import paramiko


def remove_ansi_escape_codes(text):
    """Удаляет ANSI escape-коды из текста."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def copy_files(server_config: dict[str, int], flow_dir: str, remote_dir: str, logger: Logger):
    """
    Copy pipeline files to the remote server
    """
    logger.info("🚀 Starts coping files.")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to server: {server_config["host"]}, with user: {server_config["user"]}")
        ssh.connect(
            hostname=server_config["host"],
            username=server_config["user"],
            password=server_config["password"],
        )
        logger.info("✅ Connected to the server.")

        sftp = ssh.open_sftp()

        for root, _, files in os.walk(flow_dir):
            remote_path = os.path.join(remote_dir, os.path.relpath(root, flow_dir)).replace("\\", "/")

            for file in files:
                if file.startswith("hub_"):
                    logger.warning(f"⚠️ File {file} skipped")
                    continue
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_path, file).replace("\\", "/")
                sftp.put(local_file, remote_file)
                logger.info(f"✅ File {file} copied to remote server")
        sftp.close()
        ssh.close()

    except gaierror as e:
        logger.error(f"❌ Connection error: {e}. Ensure your VPN is on and the host address is correct.")


def build_pipeline(server_config: dict[str, int], dev_env: str, logger: Logger):
    """
    Run the pipeline build on the remote server
    """
    logger.info("🚀 Starts building pipeline.")

    os.makedirs("logs", exist_ok=True)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to server: {server_config["host"]}, with user: {server_config["user"]}")
        ssh.connect(
            hostname=server_config["host"],
            username=server_config["user"],
            password=server_config["password"],
        )
        logger.info("✅ Connected to the server.")

        stdin, stdout, stderr = ssh.exec_command(f"sudo bash /app/frm_instances/forcibly_rebuild_dag.sh {dev_env}")

        stdout_text = remove_ansi_escape_codes(stdout.read().decode())
        stderr_text = remove_ansi_escape_codes(stderr.read().decode())

        with open("logs/stderr.log", "w", encoding="utf-8") as log_file:
            log_file.write(stdout_text)

        with open("logs/stdout.log", "w", encoding="utf-8") as log_file:
            log_file.write(stderr_text)

        ssh.close()
        logger.info("Pipeline built successfully, log saved to logs/")

    except gaierror as e:
        logger.error(f"❌ Connection error: {e}. Ensure your VPN is on and the host address is correct.")


def show_progress():
    """Display a simple timer while build_pipeline is running."""
    start_time = time.time()
    while not progress_done:
        elapsed = int(time.time() - start_time)
        sys.stdout.write(f"\r⏳ Building pipeline... {elapsed} sec")
        sys.stdout.flush()
        time.sleep(1)
    print("\n✅ Build completed!")


def build_pipeline_with_progress(server_config, dev_env, logger):
    """Wrapper around build_pipeline with a progress indicator."""
    global progress_done
    progress_done = False
    progress_thread = threading.Thread(target=show_progress)
    progress_thread.start()

    try:
        build_pipeline(server_config, dev_env, logger)
    finally:
        progress_done = True
        progress_thread.join()
