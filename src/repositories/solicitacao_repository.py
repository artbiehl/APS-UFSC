from repositories.base_repository import BaseRepository
from models.solicitacao import Solicitacao
from models.user import User
from sqlalchemy.sql import text


class SolicitacaoRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection)

    def add(self, solicitacao: Solicitacao):
        """
        Adiciona uma nova solicitação ao banco de dados.

        Args:
            solicitacao (Solicitacao): A solicitação a ser adicionada.
        """
        query = text("""
        INSERT INTO solicitacoes (destinatario_id, remetente_id, status)
        VALUES (:destinatario_id, :remetente_id, :status)
        """)
        self._conn.execute(
            statement=query,
            parameters={
                "destinatario_id": solicitacao.destinatario.id,
                "remetente_id": solicitacao.remetente.id,
                "status": solicitacao.status
            }
        )

    def find_by_id(self, solicitacao_id: int) -> Solicitacao | None:
        """
        Busca uma solicitação pelo ID.

        Args:
            solicitacao_id (int): O ID da solicitação.

        Returns:
            Solicitacao | None: A solicitação encontrada ou None se não existir.
        """
        query = text("""
        SELECT id, destinatario_id, remetente_id, status
        FROM solicitacoes
        WHERE id = :id
        """)
        row = self._conn.execute(
            statement=query,
            parameters={"id": solicitacao_id}
        ).fetchone()

        if row:
            # Buscando os usuários relacionados (destinatário e remetente)
            destinatario = self._find_user_by_id(row["destinatario_id"])
            remetente = self._find_user_by_id(row["remetente_id"])

            return Solicitacao(
                destinatario=destinatario,
                remetente=remetente,
                status=row["status"]
            )
        return None

    def _find_user_by_id(self, user_id: int) -> User:
        """
        Busca um usuário pelo ID. Método auxiliar para compor a solicitação.

        Args:
            user_id (int): O ID do usuário.

        Returns:
            User: O usuário encontrado.
        """
        query = text("""
        SELECT id, cpf, username, email, birthdate, encrypted_password
        FROM users
        WHERE id = :id
        """)
        row = self._conn.execute(
            statement=query,
            parameters={"id": user_id}
        ).fetchone()

        if row:
            return User(
                id=row["id"],
                cpf=row["cpf"],
                username=row["username"],
                email=row["email"],
                birthdate=row["birthdate"],
                encrypted_password=row["encrypted_password"]
            )
        raise ValueError(f"Usuário com ID {user_id} não encontrado.")