from repositories.base_repository import BaseRepository
from repositories.user_repository import UserRepository
from models.solicitacao import Solicitacao
from models.user import User
from sqlalchemy.sql import text


class SolicitacaoRepository(BaseRepository):
    def __init__(self, connection, user_repository: UserRepository = None):
        super().__init__(connection)
        # Repositório de usuários para buscar entidades User
        self._user_repository = user_repository or UserRepository(connection)

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

        if not row:
            return None

        destinatario = self._user_repository.find_by_id(row["destinatario_id"])
        remetente = self._user_repository.find_by_id(row["remetente_id"])
        solicitacao = Solicitacao(destinatario=destinatario, remetente=remetente, status=row["status"])
        setattr(solicitacao, 'id', row['id'])
        return solicitacao

    def find_by_users(self, destinatario: User, remetente: User) -> Solicitacao | None:
        """
        Busca uma solicitação pelo destinatário e remetente.

        Args:
            destinatario (User): O destinatário da solicitação.
            remetente (User): O remetente da solicitação.

        Returns:
            Solicitacao | None: A solicitação encontrada ou None se não existir.
        """
        query = text("""
        SELECT id, destinatario_id, remetente_id, status
        FROM solicitacoes
        WHERE destinatario_id = :destinatario_id AND remetente_id = :remetente_id
        """)
        row = self._conn.execute(
            statement=query,
            parameters={
                "destinatario_id": destinatario.id,
                "remetente_id": remetente.id
            }
        ).fetchone()

        if not row:
            return None

        dest = self._user_repository.find_by_id(row["destinatario_id"])
        rem = self._user_repository.find_by_id(row["remetente_id"])
        solicitacao = Solicitacao(destinatario=dest, remetente=rem, status=row["status"])
        setattr(solicitacao, 'id', row['id'])
        return solicitacao

    def update(self, solicitacao: Solicitacao):
        """
        Atualiza o status de uma solicitação no banco de dados.

        Args:
            solicitacao (Solicitacao): A solicitação com status já modificado.

        Raises:
            ValueError: Se a solicitação não tiver um ID definido.
        """
        if not hasattr(solicitacao, 'id') or getattr(solicitacao, 'id') is None:
            raise ValueError("Solicitação precisa ter um ID para atualização.")

        query = text("""
        UPDATE solicitacoes
        SET status = :status
        WHERE id = :id
        """)
        self._conn.execute(
            statement=query,
            parameters={
                "status": solicitacao.status,
                "id": solicitacao.id
            }
        )
