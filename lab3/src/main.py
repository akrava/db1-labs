from settings import DB_DIALECT, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, setup_db_logging
from controller.common import Controller

if __name__ == '__main__':
    setup_db_logging()
    controller = Controller(DB_DIALECT, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, "db1-lab3")
    controller.start()
