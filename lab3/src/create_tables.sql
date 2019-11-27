CREATE TABLE IF NOT EXISTS contragents
(
    IPN          int PRIMARY KEY,
    name         varchar(255) NOT NULL,
    phone_number char(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS cities
(
    id   serial PRIMARY KEY,
    name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouses
(
    num          serial PRIMARY KEY,
    address      text NOT NULL,
    phone_number char(15) NOT NULL,
    city_id      serial NOT NULL,
    CONSTRAINT city_id FOREIGN KEY (city_id)
        REFERENCES cities (id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS invoices
(
    num               serial PRIMARY KEY,
    date_departure    date NOT NULL,
    date_arrival      date,
    shipping_cost     money NOT NULL,
    sender_ipn        int NOT NULL,
    recipient_ipn     int NOT NULL,
    warehouse_dep_num serial NOT NULL,
    warehouse_arr_num serial NOT NULL,
    CONSTRAINT recipient_ipn FOREIGN KEY (recipient_ipn)
        REFERENCES contragents (IPN)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT sender_ipn FOREIGN KEY (sender_ipn)
        REFERENCES contragents (IPN)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT warehouse_arr_num FOREIGN KEY (warehouse_arr_num)
        REFERENCES warehouses (num)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT warehouse_dep_num FOREIGN KEY (warehouse_dep_num)
        REFERENCES warehouses (num)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS goods
(
    id          serial PRIMARY KEY,
    height      int NOT NULL,
    width       int NOT NULL,
    depth       int NOT NULL,
    weight      int NOT NULL,
    description text,
    invoice_num serial NOT NULL,
    CONSTRAINT invoice_num FOREIGN KEY (invoice_num)
        REFERENCES invoices (num)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS goods_descriptions ON goods USING gin(to_tsvector('english', description));
