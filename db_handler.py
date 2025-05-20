# db_handler.py

import sqlite3
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DBHandler:
    def __init__(self):
        self.db_path = 'work_orders.db'
        print("Using DB at:", resource_path(self.db_path))

        self.db_path = resource_path(self.db_path)
    def insert_record(self, input_text, screenshot_path):
        # conn = sqlite3.connect(self.db_path)
        # cursor = conn.cursor()
        # cursor.execute('''
        #     INSERT INTO work_orders (input_text, image_blob)
        #     VALUES (?, ?)
        # ''', (input_text, screenshot_path))
        # conn.commit()
        # conn.close()
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tables in DB:", cursor.fetchall())

    def get_all_records(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM work_orders')
        records = cursor.fetchall()
        conn.close()
        return records
    

    def fetch_records_by_work_order(self, wo_number):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, input_text, image_blob, timestamp FROM work_orders WHERE input_text = ?", (wo_number,))

        records = cursor.fetchall()
        conn.close()
        return records


    def delete_records_by_criteria(self, wo, start_date, end_date):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if wo:
            cursor.execute("""
                DELETE FROM work_orders
                WHERE input_text=? AND DATE(timestamp) BETWEEN ? AND ?
            """, (wo, start_date, end_date))
        else:
            cursor.execute("""
                DELETE FROM work_orders
                WHERE DATE(timestamp) BETWEEN ? AND ?
            """, (start_date, end_date))

        row_count = cursor.rowcount
        conn.commit()
        conn.close()
        return row_count
