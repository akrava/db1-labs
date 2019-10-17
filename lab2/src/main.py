from settings import DB_PORT, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from controller.common import Controller
import logging
import psycopg2


if __name__ == '__main__':
    logging.getLogger().setLevel("INFO")
    connection = None
    try:
        connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    except (Exception, psycopg2.Error) as e:
        logging.exception(e)
    finally:
        if connection is None:
            logging.error("Couldn't connect to database, aborting...")
            exit(1)
        else:
            logging.info(f"Opened connection with {DB_NAME} on {DB_HOST}:{DB_PORT}",)
    controller = Controller(connection, "db1-lab2")
    controller.start()
    connection.close()
