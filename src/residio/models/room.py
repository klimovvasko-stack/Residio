from dataclasses import dataclass


@dataclass
class Room:
    room_id: int
    number: int
    floor: int
    capacity: int