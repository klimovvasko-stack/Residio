from database.database import get_connection
from models.room import Room


def _map(row) -> Room: # преобразует картеж из бд в обьект Room 
    return Room(*row)

# выполняет SQL запрос, для возвращения списка обьектов Room
def get_all() -> list[Room]: 
    conn = get_connection() # возвращает открытый обьект соединения 
    cur = conn.cursor() # подключение курсора для запросов 
    cur.execute("""
        SELECT room_id, number, floor, capacity
        FROM rooms
        ORDER BY number
    """)
    rows = cur.fetchall() # забирает все строчки, которая бд нашла по запросу 
    conn.close() # закрытие соединения с базой 
    return [_map(r) for r in rows]

# функция ищет конкретную комнату по её id 
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

# функция ищет конкретную комнату по её номеру 
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

# выполняет запрос INSERT для добавления новой комнаты в бд 
def create(number: int, floor: int, capacity: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rooms (number, floor, capacity)
        VALUES (?, ?, ?)
    """, (number, floor, capacity))
    room_id = cur.lastrowid # получение сгенерированного id
    conn.commit() # сохранение изменений 
    conn.close()
    return room_id 


# функция изменяет уже существующую комнату через запрос UPDATE
def update(room_id: int, number: int, floor: int, capacity: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE rooms
        SET number = ?, floor = ?, capacity = ?
        WHERE room_id = ?
    """, (number, floor, capacity, room_id))
    conn.commit() # сохранение изменений 
    conn.close()

# удаление комнаты из таблицы с помощью запроса DELETE
def delete(room_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM rooms
        WHERE room_id = ?
    """, (room_id,))
    conn.commit() # сохранение изменений
    conn.close()