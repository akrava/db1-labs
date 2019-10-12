from settings import DB_PORT, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
import psycopg2
import logging
# ----
from model.invoice import Invoice, InvoiceModel
from model.contragent import Contragent, ContragentModel
from datetime import date
from decimal import Decimal
# ---

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
    # ---
    t1 = Invoice(date(2019, 10, 11), Decimal(12000), 1, 2, 1, 2)
    t3 = Invoice(date(2019, 10, 10), Decimal(1200), 2, 1, 4, 3, date(2019, 10, 26))
    t11 = Invoice(date(2017, 10, 9), Decimal(440), 2, 1, 3, 2)
    t31 = Invoice(date(2017, 10, 10), Decimal(678), 1, 2, 4, 1, date(2017, 10, 26))
    t2 = Invoice(date(2019, 10, 10), Decimal(1200), 1, 2, 1, 2, date(2019, 10, 26), 3)
    in_m = InvoiceModel(connection)
    # print(in_m.count_all())
    # print(in_m.create(t1))
    # print(in_m.create(t3))
    # print(in_m.create_many([t11, t31]))
    # print(in_m.read(9))
    # print(in_m.read(10))
    # a = in_m.read_all(0)
    # for cur in a:
    #    print(cur)
    # t1.num = 9
    # t1.date_arrival = date(2048, 12, 12)
    # in_m.delete(9)
    # print(in_m.count_all())
    c1 = Contragent(123, "arka", "rerrrrrrrrrr46456456456456456456456")
    print(c1.__dict__)
    # ---
    connection.close()
    logging.info("Connection closed with db")
