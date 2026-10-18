from database.database import get_connection
from models.student import Student


def _map(row) -> Student:
    return Student(*row)


def get_all() -> list[Student]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.full_name, s.group_name, s.room_id, s.user_id,
               rm.number, u.login
        FROM students s
        LEFT JOIN rooms rm ON s.room_id = rm.room_id
        LEFT JOIN users u ON s.user_id = u.user_id
        ORDER BY s.student_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_id(student_id: int) -> Student | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.full_name, s.group_name, s.room_id, s.user_id,
               rm.number, u.login
        FROM students s
        LEFT JOIN rooms rm ON s.room_id = rm.room_id
        LEFT JOIN users u ON s.user_id = u.user_id
        WHERE s.student_id = ?
    """, (student_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_user_id(user_id: int) -> Student | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.full_name, s.group_name, s.room_id, s.user_id,
               rm.number, u.login
        FROM students s
        LEFT JOIN rooms rm ON s.room_id = rm.room_id
        LEFT JOIN users u ON s.user_id = u.user_id
        WHERE s.user_id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_room_id(room_id: int) -> list[Student]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.full_name, s.group_name, s.room_id, s.user_id,
               rm.number, u.login
        FROM students s
        LEFT JOIN rooms rm ON s.room_id = rm.room_id
        LEFT JOIN users u ON s.user_id = u.user_id
        WHERE s.room_id = ?
        ORDER BY s.full_name
    """, (room_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def create(full_name: str, group_name: str, room_id: int | None, user_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO students (full_name, group_name, room_id, user_id)
        VALUES (?, ?, ?, ?)
    """, (full_name, group_name, room_id, user_id))
    student_id = cur.lastrowid
    conn.commit()
    conn.close()
    return student_id


def update(student_id: int, full_name: str, group_name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students
        SET full_name = ?, group_name = ?
        WHERE student_id = ?
    """, (full_name, group_name, student_id))
    conn.commit()
    conn.close()


def update_room(student_id: int, room_id: int | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students
        SET room_id = ?
        WHERE student_id = ?
    """, (room_id, student_id))
    conn.commit()
    conn.close()


def delete(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM students
        WHERE student_id = ?
    """, (student_id,))
    conn.commit()
    conn.close()