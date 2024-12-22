import sqlite3

class SQLiteDataSink:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.initialize_table()

    def initialize_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_data (
                asset_id TEXT,
                attribute_id TEXT,
                timestamp TEXT,
                value TEXT
            )
        """)
        self.connection.commit()

    def write_message(self, message):
        self.cursor.execute("""
            INSERT INTO processed_data (asset_id, attribute_id, timestamp, value)
            VALUES (?, ?, ?, ?)
        """, (message["asset_id"], message["attribute_id"], message["timestamp"], message["value"]))
        self.connection.commit()

    def close(self):
        self.connection.close()
