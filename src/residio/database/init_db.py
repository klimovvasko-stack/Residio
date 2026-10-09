import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
DB_PATH = BASE_DIR / "residio.db"


def init_db():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        script = f.read()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(script)
        conn.commit()
    finally:
        conn.close()


def show_table(name):
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(f"SELECT * FROM {name}").fetchall()
    finally:
        conn.close()

    print(f"--- {name} ---")
    for row in rows:
        print(row)


if __name__ == "__main__":
    init_db()
    for table in ("user_roles", "rooms", "users", "students"):
        show_table(table)

# python init_db.py