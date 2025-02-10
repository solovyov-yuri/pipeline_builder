import os

import oracledb
import psycopg2


def execute_sql_file(cursor, file_path, logger):
    """Читает и выполняет SQL-файл."""
    # cursor.execute("DROP TABLE IF EXISTS rdv.mart_payment_sb_cmtifo_bsi_c2_kroc;")
    with open(file_path, "r", encoding="utf-8") as file:
        sql = file.read()
        logger.info(f"Выполняем {file_path}...")
        cursor.execute(sql)


def create_or_update_entities(ddl_dir, gp_db_config, logger):
    """ """
    gp_ddl_dir = f"{ddl_dir}\\gp"
    sql_files = sorted(file for file in os.listdir(gp_ddl_dir) if file.endswith(".sql"))

    if not sql_files:
        logger.warning("Нет SQL-файлов для выполнения.")
        return

    try:
        conn = psycopg2.connect(**gp_db_config)
        conn.autocommit = True  # Автоматическое применение транзакций
        cursor = conn.cursor()

        for sql_file in sql_files:
            file_path = os.path.join(gp_ddl_dir, sql_file)
            print(file_path)
            execute_sql_file(cursor, file_path, logger)

        logger.info("Tables created")

    except Exception as e:
        logger.error(f"Ошибка выполнения SQL: {e}")

    finally:
        cursor.close()
        conn.close()


def create_oracle_entities(ddl_dir, oracle_config, logger):
    """ """
    oracle_ddl_dir = f"{ddl_dir}\\oracle"
    sql_files = sorted(file for file in os.listdir(oracle_ddl_dir) if file.endswith(".sql"))
    logger.info(f"Found files: {sql_files}")

    if not sql_files:
        logger.warning("Нет SQL-файлов для выполнения.")
        return

    try:
        conn = oracledb.connect(**oracle_config)
        cursor = conn.cursor()
        logger.info("Conn success!")

        for sql_file in sql_files:
            file_path = os.path.join(oracle_ddl_dir, sql_file)
            print(file_path)
            execute_sql_file(cursor, file_path, logger)

        logger.info("Tables created")

    except Exception as e:
        logger.error(f"Ошибка выполнения SQL: {e}")

    finally:
        cursor.close()
        conn.close()
