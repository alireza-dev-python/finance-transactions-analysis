daily_logs = [
    {"id": "tx_1001", "name": "Ali Alavi", "user_id": "u001", "amount": 250000.0, "status": "SUCCESS", "timestamp": "2026-05-24 10:05:00"},
    {"id": "tx_1002", "name": "Ali Alavi", "user_id": "u001", "amount": 150000.0, "status": "FAILED", "timestamp": "2026-05-24 10:10:00"},
    {"id": "tx_1003", "name": "Ali Alavi", "user_id": "u001", "amount": 175000.0, "status": "FAILED", "timestamp": "2026-05-24 10:20:00"},
    {"id": "tx_1004", "name": "Ali Alavi", "user_id": "u001", "amount": 90000.0, "status": "FAILED", "timestamp": "2026-05-24 10:30:00"},
    {"id": "tx_1005", "name": "Ali Alavi", "user_id": "u001", "amount": 300000.0, "status": "FAILED", "timestamp": "2026-05-24 10:40:00"},
    
    {"id": "tx_2001", "name": "Sara Rezaei", "user_id": "u002", "amount": 50000.0, "status": "SUCCESS", "timestamp": "2026-05-24 11:00:00"},
    {"id": "tx_2002", "name": "Sara Rezaei", "user_id": "u002", "amount": 70000.0, "status": "FAILED", "timestamp": "2026-05-24 11:05:00"},
    
    {"id": "tx_3001", "name": "Reza Mohammadi", "user_id": "u003", "amount": 1000000.0, "status": "FAILED", "timestamp": "2026-05-24 12:00:00"},
    {"id": "tx_3002", "name": "Reza Mohammadi", "user_id": "u003", "amount": 1000000.0, "status": "FAILED", "timestamp": "2026-05-24 12:10:00"},
    {"id": "tx_3003", "name": "Reza Mohammadi", "user_id": "u003", "amount": 1000000.0, "status": "FAILED", "timestamp": "2026-05-24 12:20:00"},
    {"id": "tx_3004", "name": "Reza Mohammadi", "user_id": "u003", "amount": 1000000.0, "status": "FAILED", "timestamp": "2026-05-24 12:30:00"}
]


import json
import sqlite3

with open("daily_logs.json", "w", encoding = "utf-8") as file:
    for record in daily_logs:
        file.write(json.dumps(record) + "\n")

def load_json_to_db(filename):
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect("finance_transactions.db")
        conn.execute("PRAGMA journal_mode = WAL")
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS transactions")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id            TEXT PRIMARY KEY,
                name          TEXT,
                user_id       Text,
                amount        REAL,
                status        TEXT,
                timestamp     DATETIME
                )
                """)

        with conn:
            with open(filename, "r", encoding = "utf-8") as file:
                for line in file:
                    if not line.strip():
                        continue

                    try:
                        record = json.loads(line)

                        cursor.execute("""
                            INSERT INTO transactions
                            (id, name, user_id, amount, status, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                            record["id"],
                            record["name"],
                            record["user_id"],
                            record["amount"],
                            record["status"],
                            record["timestamp"]
                        ))
                    except json.JSONDecodeError:
                        print("Error:")
    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


def get_high_risk_users():
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect("finance_transactions.db")
        cursor = conn.cursor()

        query = """
            SELECT
                name,
                user_id,
                strftime('%Y-%m-%d %H:00:00', timestamp) AS hour_bucket,
                COUNT(*) AS failed_count
            FROM transactions
            WHERE status = "FAILED"
            GROUP BY user_id, hour_bucket
            HAVING failed_count > 3
            """

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("There is not any dangerous customer")
        else:
            for row in results:
                print(row)
                
    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()
        

load_json_to_db("daily_logs.json")
get_high_risk_users()        


