import sqlite3 
import datetime
from pathlib import Path

DATABASE = Path(__file__).resolve().with_name("RSL_PROD.db")


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_database_connection():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.execute("PRAGMA busy_timeout = 10000")
    connection.execute("PRAGMA journal_mode = WAL")
    return connection

def check_config():
    db = get_database_connection()
    
    try:
           cursor = db.cursor()
   
           cursor.execute("""
               SELECT register_open
               FROM config
           """)
   
           result = cursor.fetchone()
           return result[0] if result else None 
       
    finally:
        db.close()

def add_user(discord_id, username):
    db = get_database_connection()

    try:
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO users (username, discord_id)
            VALUES (?, ?)
        """, (username, str(discord_id)))

        db.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        db.rollback()
        print(f"[DATABASE ERROR] {error}")
        return None

    finally:
        db.close()
        
def get_user(discord_id):
    db = get_database_connection()

    try:
        cursor = db.cursor()

        cursor.execute("""
            SELECT user_id, username, home_dir, paid
            FROM users
            WHERE discord_id = ?
        """, (str(discord_id),))

        return cursor.fetchone()

    finally:
        db.close()