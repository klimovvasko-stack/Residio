from database.database import get_connection
from models.room import Room


def _map(row) -> Room:
    return Room(*row)


def get_all() -> list[Room]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT room_id, number, floor, capacity
        FROM rooms
        ORDER BY number
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_id(room_id: int) -> Room | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT room_id, number, floor, capacity
        FROM rooms
        WHERE room_id = ?
    """, (room_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_number(number: int) -> Room | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT room_id, number, floor, capacity
        FROM rooms
        WHERE number = ?
    """, (number,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def create(number: int, floor: int, capacity: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rooms (number, floor, capacity)
        VALUES (?, ?, ?)
    """, (number, floor, capacity))
    room_id = cur.lastrowid
    conn.commit()
    conn.close()
    return room_id


def update(room_id: int, number: int, floor: int, capacity: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE rooms
        SET number = ?, floor = ?, capacity = ?
        WHERE room_id = ?
    """, (number, floor, capacity, room_id))
    conn.commit()
    conn.close()


def delete(room_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM rooms
        WHERE room_id = ?
    """, (room_id,))
    conn.commit()
    conn.close()