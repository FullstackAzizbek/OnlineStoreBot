import sqlite3
from config import db_name


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_category(self):
        self.cursor.execute(
            "SELECT id, category_name FROM categories;"
        )
        categories = self.cursor.fetchall()
        return categories

    def add_category(self, new_category):
        try:
            self.cursor.execute(
                "INSERT INTO categories (category_name) VALUES (?);",
                (new_category,)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Error adding category:", e)
            return False

    def check_category_exists(self, name):
        self.cursor.execute(
            "SELECT * FROM categories WHERE category_name = ?;", (name,)
        )
        lst = self.cursor.fetchall()

        if not lst:
            return True
        else:
            return False

    def del_category(self, name):
        try:
            self.cursor.execute(
                f"DELETE FROM categories WHERE category_name = ?;", (name,)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False

    def update_category(self, new_name, old_name):
        try:
            self.cursor.execute(
                f"UPDATE categories SET category_name = ? WHERE category_name = ?;", (new_name, old_name,)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            return False


    def add_product(self, pro_name, pro_desc, pro_price, pro_cat, pro_image, pro_phone, pro_owner):
        try:
            self.cursor.execute(
                f"INSERT INTO products(product_name, product_desc, product_price, product_category, product_image, phone, owner) VALUES (?, ?, ?, ?, ?, ?, ?);", 
                (pro_name, pro_desc, pro_price, pro_cat, pro_image, pro_phone, pro_owner)
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def get_products(self, tg_id):
        self.cursor.execute(
            "SELECT product_name, product_desc, product_price, product_category, product_image, phone, id FROM products WHERE owner = ?;", (tg_id,)
        )
        products = self.cursor.fetchall()

        return products
    
    def get_edit_product(self, product_name, product_desc, product_price, product_category, product_image, phone, pro_id):
        self.cursor.execute(
            "UPDATE products SET product_name = %s, product_desc = %s, product_price = %s, product_category = %s, product_image = %s, phone = %s WHERE id = %s;",
            (product_name, product_desc, product_price, product_category, product_image, phone, pro_id,)
        )
        self.conn.commit()
 
