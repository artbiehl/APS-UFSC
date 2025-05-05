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
            solicitacao_repository (SolicitacaoRepository, opcional): 
                Repositório para persistência das solicitações.
        """
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
        if not isinstance(destinatario, User):
            raise TypeError("O destinatário deve ser uma instância de User.")
        if not isinstance(remetente, User):
            raise TypeError("O remetente deve ser uma instância de User.")
        
        if destinatario == remetente:
            raise ValueError("O destinatário e o remetente não podem ser a mesma pessoa.")
        
        # Cria a solicitação
        solicitacao = Solicitacao(destinatario=destinatario, remetente=remetente)
        
        # Persiste a solicitação no repositório
        self._solicitacao_repository.add(solicitacao)
        
        return solicitacao

    def aceitar(self, solicitacao: Solicitacao) -> Solicitacao:
        """
        Aceita uma solicitação existente.

        Args:
            solicitacao (Solicitacao): A solicitação a ser aceita.

        Returns:
            Solicitacao: A solicitação com status atualizado.

        Raises:
            TypeError: Se o parâmetro não for uma instância de Solicitacao.
            ValueError: Se a solicitação já tiver sido processada.
        """
        # validação de tipo
        if not isinstance(solicitacao, Solicitacao):
            raise TypeError("O argumento deve ser uma instância de Solicitacao.")
        # só aceita se estiver pendente
        if solicitacao.status != "Pendente":
            raise ValueError("Solicitação já foi processada.")
        # atualiza status
        solicitacao.status = "Aceita"
        # persiste alteração no banco
        self._solicitacao_repository.update(solicitacao)
        return solicitacao

    def recusar(self, solicitacao: Solicitacao) -> Solicitacao:
        """
        Recusa uma solicitação existente.

        Args:
            solicitacao (Solicitacao): A solicitação a ser recusada.

        Returns:
            Solicitacao: A solicitação com status atualizado.

        Raises:
            TypeError: Se o parâmetro não for uma instância de Solicitacao.
            ValueError: Se a solicitação já tiver sido processada.
        """
        if not isinstance(solicitacao, Solicitacao):
            raise TypeError("O argumento deve ser uma instância de Solicitacao.")
        if solicitacao.status != "Pendente":
            raise ValueError("Solicitação já foi processada.")
        solicitacao.status = "Recusada"
        self._solicitacao_repository.update(solicitacao)
        return solicitacao
