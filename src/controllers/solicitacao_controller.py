from models.solicitacao import Solicitacao
from models.user import User
from repositories.solicitacao_repository import SolicitacaoRepository


class SolicitacaoController:
    """
    Controlador para gerenciar as solicitações no sistema.

    Métodos:
        enviar(destinatario, remetente): Envia uma nova solicitação.
        aceitar(solicitacao): Aceita uma solicitação existente.
        recusar(solicitacao): Recusa uma solicitação existente.
    """

    def __init__(self, solicitacao_repository: SolicitacaoRepository = None):
        """
        Inicializa o controlador de solicitações.

        Args:
            solicitacao_repository (SolicitacaoRepository, opcional): Repositório para persistência das solicitações.
        """
        # Usa o repositório fornecido ou instancia o padrão
        self._solicitacao_repository = solicitacao_repository or SolicitacaoRepository()

    def enviar(self, destinatario: User, remetente: User) -> Solicitacao:
        """
        Envia uma nova solicitação.

        Args:
            destinatario (User): O usuário que receberá a solicitação.
            remetente (User): O usuário que enviará a solicitação.

        Returns:
            Solicitacao: A solicitação criada e persistida.
        """
        solicitacao = Solicitacao(destinatario=destinatario, remetente=remetente)
        self._solicitacao_repository.add(solicitacao)
        return solicitacao

    def aceitar(self, solicitacao: Solicitacao):
        """
        Aceita uma solicitação existente.

        Args:
            solicitacao (Solicitacao): A solicitação a ser aceita.

        Raises:
            ValueError: Se a solicitação já tiver sido processada.
        """
        if solicitacao.status != "Pendente":
            raise ValueError("Solicitação já foi processada.")
        solicitacao.status = "Aceita"
        self._solicitacao_repository.update(solicitacao)

    def recusar(self, solicitacao: Solicitacao):
        """
        Recusa uma solicitação existente.

        Args:
            solicitacao (Solicitacao): A solicitação a ser recusada.

        Raises:
            ValueError: Se a solicitação já tiver sido processada.
        """
        if solicitacao.status != "Pendente":
            raise ValueError("Solicitação já foi processada.")
        solicitacao.status = "Recusada"
        self._solicitacao_repository.update(solicitacao)
