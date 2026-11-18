from database.database import open_connection
from models.user import User



def _map(row) -> User:
    return User(*row)

# получение списка всех пользователей системы 
def find_all_users() -> list[User]:
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.login, u.password, u.user_role, r.name
        FROM users u
        LEFT JOIN user_roles r ON u.user_role = r.user_role_id
        ORDER BY u.user_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

# ищет учетную запись по id
def find_user_by_id(user_id: int) -> User | None:
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.login, u.password, u.user_role, r.name
        FROM users u
        LEFT JOIN user_roles r ON u.user_role = r.user_role_id
        WHERE u.user_id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

# поиск по авторизации
def find_user_by_login(login: str) -> User | None:
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.login, u.password, u.user_role, r.name
        FROM users u
        LEFT JOIN user_roles r ON u.user_role = r.user_role_id
        WHERE u.login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

# создает новую учетную запись 
def add_user(login: str, password: str, user_role: int) -> int:
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (login, password, user_role)
        VALUES (?, ?, ?)
    """, (login, password, user_role))
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return user_id

# удаляет учетную запись 
def remove_user(user_id: int):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM users
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()
