# db_handler.py

import sqlite3
import os

class DBHandler:
    def __init__(self):
        self.db_path = 'data/work_orders.db'
    
    def insert_record(self, input_text, screenshot_path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO work_orders (input_text, image_blob)
            VALUES (?, ?)
        ''', (input_text, screenshot_path))
        conn.commit()
        conn.close()

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

