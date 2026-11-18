from database.database import open_connection
from models.user_role import UserRole


def _map(row) -> UserRole:
    return UserRole(*row)

# делает запрос, чтобы извлечь все существующие роли из таблицы 
def find_all_roles() -> list[UserRole]:
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_role_id, name
        FROM user_roles
        ORDER BY user_role_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

# ищет в базе роль по её id
def find_role_by_id(role_id: int) -> UserRole | None:
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_role_id, name
        FROM user_roles
        WHERE user_role_id = ?
    """, (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
