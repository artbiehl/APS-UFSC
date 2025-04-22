from models.solicitacao import Solicitacao
from models.user import User


class SolicitacaoController:
    """
    Controlador para gerenciar as solicitações no sistema.

    Métodos:
        enviar(destinatario, remetente): Envia uma nova solicitação.
        aceitar(solicitacao): Aceita uma solicitação existente.
        recusar(solicitacao): Recusa uma solicitação existente.
    """

    def enviar(self, destinatario: User, remetente: User) -> Solicitacao:
        """
        Envia uma nova solicitação.

        Args:
            destinatario (User): O usuário que receberá a solicitação.
            remetente (User): O usuário que enviará a solicitação.

        Returns:
            Solicitacao: A solicitação criada.
        """
        solicitacao = Solicitacao(destinatario=destinatario, remetente=remetente)
        # logica para persistir a solicitação no banco de dados
        return solicitacao

    def aceitar(self, solicitacao: Solicitacao):
        """
        Aceita uma solicitação existente.

        Args:
            solicitacao (Solicitacao): A solicitação a ser aceita.
        """
        pass  # thives implementa

    def recusar(self, solicitacao: Solicitacao):
        """
        Recusa uma solicitação existente.

        Args:
            solicitacao (Solicitacao): A solicitação a ser recusada.
        """
        pass  # thives implementa