import sqlite3
from db.queries import *
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_PRODUCTS)
    conn.commit()
    conn.close()

def add_products_db(product_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(ADD_PRODUCT, (product_name,))
    conn.commit()
    last_row_id = cursor.lastrowid
    conn.close()
    return last_row_id

def get_product():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(GET_PRODUCTS)
    products = cursor.fetchall()  
    conn.close()
    return products

def update_product_db(product_id, new_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(UPDATE_PRODUCT, (new_name, product_id))
    conn.commit()
    conn.close()

def toggle_product_status(product_id, is_checked):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(TOGGLE_PRODUCT_STATUS, (int(is_checked), product_id))
    conn.commit()
    conn.close()

def delete_product_db(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(DELETE_PRODUCT, (product_id,))
    conn.commit()
    conn.close()