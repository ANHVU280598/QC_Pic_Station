import sqlite3

def init_database():
    db_path = 'data/work_orders.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT,
                image_blob BLOB,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully: work_orders.db")

if __name__ == "__main__":
    init_database()
