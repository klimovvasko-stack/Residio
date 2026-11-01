from dataclasses import dataclass

@dataclass
class UserRole:
    user_role_id: int   # первичный ключ 
    name: str           # название роли 