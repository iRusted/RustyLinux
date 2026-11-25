import sqlite3 
import datetime

DATABASE = "RSL_PROD.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_database_connection():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.execute("PRAGMA busy_timeout = 10000")
    connection.execute("PRAGMA journal_mode = WAL")
    return connection

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

    except sqlite3.IntegrityError:
        db.rollback()
        return None

    finally:
        db.close()