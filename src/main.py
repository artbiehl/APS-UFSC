import tkinter as tk
from datetime import date  # Import necessário para lidar com datas
from sqlalchemy import create_engine  # Import para criar a conexão com o banco de dados
from controllers.solicitacao_controller import SolicitacaoController
from models.user import User
from models.solicitacao import Solicitacao
from views.solicitacao_view import SolicitacaoView
from repositories.solicitacao_repository import SolicitacaoRepository


# Criando a conexão com o banco de dados
engine = create_engine('sqlite:///database.db')  # Substitua pelo seu banco de dados
connection = engine.connect()

# Função de callback para o botão "Voltar"
def voltar_callback():
    print("Botão 'Voltar' clicado!")

# Simulando o controlador
class MockSolicitacaoController(SolicitacaoController):
    def __init__(self):
        super().__init__(SolicitacaoRepository(connection))

    def aceitar(self, solicitacao):
        print(f"Solicitação de {solicitacao.remetente.username} aceita!")

    def recusar(self, solicitacao):
        print(f"Solicitação de {solicitacao.remetente.username} recusada!")

# Criando usuários para teste
user1 = User(
    cpf="12345678901",
    username="user1",
    email="user1@example.com",
    birthdate=date(2000, 1, 1),  
    encrypted_password="password1"
)
user2 = User(
    cpf="98765432109",
    username="user2",
    email="user2@example.com",
    birthdate=date(1995, 5, 5),  
    encrypted_password="password2"
)

# Criando solicitações para teste
solicitacoes = [
    Solicitacao(destinatario=user2, remetente=user1),
    Solicitacao(destinatario=user1, remetente=user2),
]



# Inicializando a interface
if __name__ == "__main__":
    root = tk.Tk()
    controller = MockSolicitacaoController()
    app = SolicitacaoView(root, solicitacoes, voltar_callback, controller)
    root.mainloop()