# user_controller.py
from models.user import User
from repositories.user_repository import UserRepository
from datetime import date
from utils.encryption import cipher


class UserController:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(self, cpf: str, username: str, email: str, birthdate: date, password: str):
        encrypted_password = cipher.encrypt(password.encode('utf-8')).decode('utf-8')
        user = User(
            cpf=cpf,
            username=username,
            email=email,
            birthdate=birthdate,
            encrypted_password=encrypted_password
        )
        self._user_repository.add(user)

    def get_user_by_username(self, username: str) -> dict:
        user = self._user_repository.find_by_username(username)
        return {
            "id": user.id,
            "username": user.username
        }

    def login(self, username: str, password: str) -> dict:

        user = self._user_repository.find_by_username(username)
        if user is None:
            raise ValueError("Usuário não encontrado.")


        decrypted = cipher.decrypt(user.encrypted_password.encode('utf-8')).decode('utf-8')
        if decrypted != password:
            raise ValueError("Senha incorreta.")

        return {"id": user.id, "username": user.username}
