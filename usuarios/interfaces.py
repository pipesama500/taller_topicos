# usuarios/interfaces.py
from abc import ABC, abstractmethod

class RoleManager(ABC):
    @abstractmethod
    def create_role(self, name: str):
        pass

    @abstractmethod
    def get_role_by_name(self, name: str):
        pass

    @abstractmethod
    def assign_role_to_user(self, user_id: int, role_id: int):
        pass
