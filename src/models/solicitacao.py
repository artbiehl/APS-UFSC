from typing import Optional
from .user import User


class Solicitacao:
    """
    Modelo para representar uma solicitação no sistema.

    Atributos:
        destinatario (User): O usuário que receberá a solicitação.
        remetente (User): O usuário que enviou a solicitação.
        status (str): O status atual da solicitação (ex.: "Pendente", "Aceita", "Recusada").
    """

    def __init__(
        self,
        destinatario: User,
        remetente: User,
        status: Optional[str] = "Pendente",
    ):
        self.destinatario = destinatario
        self.remetente = remetente
        self.status = status

    @property
    def destinatario(self) -> User:
        return self._destinatario

    @destinatario.setter
    def destinatario(self, value: User):
        if not isinstance(value, User):
            raise TypeError("Destinatário deve ser uma instância da classe User.")
        self._destinatario = value

    @property
    def remetente(self) -> User:
        return self._remetente

    @remetente.setter
    def remetente(self, value: User):
        if not isinstance(value, User):
            raise TypeError("Remetente deve ser uma instância da classe User.")
        self._remetente = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in ["Pendente", "Aceita", "Recusada"]:
            raise ValueError("Status deve ser 'Pendente', 'Aceita' ou 'Recusada'.")
        self._status = value