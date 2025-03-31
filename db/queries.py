CREATE_TABLE_PRODUCTS = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    is_checked INTEGER DEFAULT 0
);
"""

ADD_PRODUCT = "INSERT INTO products (product) VALUES (?);"

GET_PRODUCTS = "SELECT id, product, is_checked FROM products;"

UPDATE_PRODUCT = "UPDATE products SET product = ? WHERE id = ?;"

TOGGLE_PRODUCT_STATUS = "UPDATE products SET is_checked = ? WHERE id = ?;"

DELETE_PRODUCT = "DELETE FROM products WHERE id = ?;"