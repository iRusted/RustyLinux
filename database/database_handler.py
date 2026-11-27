
import sqlite3
from pathlib import Path


# =====================================================
# DATABASE CONFIGURATION
# =====================================================

DATABASE = Path(__file__).resolve().with_name("RSL_PROD.db")


# =====================================================
# DATABASE SCHEMA
# =====================================================

SCHEMA = {
    "config": """
        CREATE TABLE config (
            register_open INTEGER NOT NULL DEFAULT 0
        )
    """,

    "users": """
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            home_dir TEXT NOT NULL UNIQUE,
            paid INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            policy_agreed INTEGER NOT NULL DEFAULT 0,
            policy_agreed_at TEXT DEFAULT NULL,
            policy_version TEXT DEFAULT NULL
        )
    """
}


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_database_connection():
    """Create a database connection."""

    connection = sqlite3.connect(
        DATABASE,
        timeout=10
    )

    connection.execute("PRAGMA busy_timeout = 10000")

    return connection


# =====================================================
# DATABASE INITIALIZATION
# =====================================================

def check_database() -> dict:
    """Create and validate the RustyLinux database."""

    result = {
        "success": False,
        "created_database": False,
        "created_tables": [],
        "created_columns": [],
        "errors": []
    }

    try:
        result["created_database"] = not DATABASE.exists()

        DATABASE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with get_database_connection() as db:

            # Enable WAL during initialization
            db.execute("PRAGMA journal_mode = WAL")

            # Create missing tables
            for table, create_statement in SCHEMA.items():

                exists = db.execute(
                    """
                    SELECT 1
                    FROM sqlite_master
                    WHERE type = 'table'
                    AND name = ?
                    """,
                    (table,)
                ).fetchone()

                if not exists:
                    db.execute(create_statement)
                    result["created_tables"].append(table)

            # Expected columns
            expected_columns = {
                "config": {
                    "register_open": ("INTEGER", 0)
                },
                "users": {
                    "user_id": ("INTEGER", None),
                    "discord_id": ("TEXT", None),
                    "username": ("TEXT", None),
                    "home_dir": ("TEXT", None),
                    "paid": ("INTEGER", 0),
                    "created_at": ("TEXT", None),
                    "policy_agreed": ("INTEGER", 0),
                    "policy_agreed_at": ("TEXT", None),
                    "policy_version": ("TEXT", None)
                }
            }

            # Check existing columns
            for table, columns in expected_columns.items():

                existing = db.execute(
                    f"PRAGMA table_info({table})"
                ).fetchall()

                existing_names = {
                    column[1] for column in existing
                }

                for column, (data_type, default) in columns.items():

                    if column in existing_names:
                        continue

                    # These columns require table-level constraints.
                    if column in (
                        "user_id",
                        "discord_id",
                        "username",
                        "home_dir"
                    ):
                        result["errors"].append(
                            f"Missing constrained column: {table}.{column}"
                        )
                        continue

                    # CURRENT_TIMESTAMP cannot be used as an
                    # ALTER TABLE default in SQLite.
                    if column == "created_at":
                        db.execute(
                            f"ALTER TABLE {table} "
                            f"ADD COLUMN {column} TEXT"
                        )

                        db.execute(
                            f"""
                            UPDATE {table}
                            SET created_at = CURRENT_TIMESTAMP
                            WHERE created_at IS NULL
                            """
                        )

                    elif default is not None:
                        db.execute(
                            f"""
                            ALTER TABLE {table}
                            ADD COLUMN {column}
                            {data_type} NOT NULL DEFAULT {default}
                            """
                        )

                    else:
                        db.execute(
                            f"""
                            ALTER TABLE {table}
                            ADD COLUMN {column} {data_type}
                            """
                        )

                    result["created_columns"].append(
                        f"{table}.{column}"
                    )

            # Ensure config has an initial row
            config_exists = db.execute(
                "SELECT 1 FROM config LIMIT 1"
            ).fetchone()

            if not config_exists:
                db.execute(
                    "INSERT INTO config (register_open) VALUES (0)"
                )

            # Verify database integrity
            integrity = db.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            if integrity != "ok":
                result["errors"].append(
                    f"Integrity check failed: {integrity}"
                )

            result["success"] = not result["errors"]

    except sqlite3.Error as error:
        result["errors"].append(str(error))

    return result


# =====================================================
# CONFIGURATION
# =====================================================

def check_config():
    """Return the current registration setting."""

    db = get_database_connection()

    try:
        cursor = db.execute(
            """
            SELECT register_open
            FROM config
            LIMIT 1
            """
        )

        result = cursor.fetchone()

        return result[0] if result else None

    finally:
        db.close()


def set_registration_status(status: bool) -> bool:
    """Enable or disable registration."""

    db = get_database_connection()

    try:
        db.execute(
            """
            UPDATE config
            SET register_open = ?
            """,
            (int(status),)
        )

        db.commit()
        return True

    except sqlite3.Error as error:
        db.rollback()
        print(f"[DATABASE ERROR] {error}")
        return False

    finally:
        db.close()


# =====================================================
# USER MANAGEMENT
# =====================================================

def add_user(discord_id, username, home_dir=None):
    """Add a new RustyLinux application account."""

    if home_dir is None:
        home_dir = str(Path("/home") / username)

    db = get_database_connection()

    try:
        cursor = db.execute(
            """
            INSERT INTO users (
                username,
                discord_id,
                home_dir
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                str(discord_id),
                str(home_dir)
            )
        )

        db.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        db.rollback()
        print(f"[DATABASE ERROR] {error}")
        return None

    except sqlite3.Error as error:
        db.rollback()
        print(f"[DATABASE ERROR] {error}")
        return None

    finally:
        db.close()


def get_user(discord_id):
    """Retrieve a user by Discord ID."""

    db = get_database_connection()

    try:
        cursor = db.execute(
            """
            SELECT
                user_id,
                username,
                home_dir,
                paid
            FROM users
            WHERE discord_id = ?
            """,
            (str(discord_id),)
        )

        return cursor.fetchone()

    finally:
        db.close()
