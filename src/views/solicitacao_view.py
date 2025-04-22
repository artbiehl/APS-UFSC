import tkinter as tk
from tkinter import messagebox
import sys
import os
import datetime


class SolicitacaoView:
    def __init__(self, root, solicitacoes, voltar_callback, controller):
        """
        Inicializa a tela de solicitações de amizade.

        Args:
            root (tk.Tk): Janela principal.
            solicitacoes (list): Lista de solicitações no formato [{"username": str, "solicitacao": Solicitacao}, ...].
            voltar_callback (function): Função chamada ao clicar no botão "Voltar".
            controller (SolicitacaoController): Controlador responsável pela lógica de solicitações.
        """
        self.root = root
        self.controller = controller
        self.root.title("Amizades")

        # Título no topo
        tk.Label(root, text="Amizades", font=("Arial", 16, "bold")).pack(pady=10)

        # Botão de voltar no canto superior direito
        voltar_button = tk.Button(root, text="Voltar", command=voltar_callback)
        voltar_button.place(relx=0.9, rely=0.05)

        # Frame para as solicitações
        self.solicitacoes_frame = tk.Frame(root)
        self.solicitacoes_frame.pack(pady=20)

        # Exibir as solicitações
        self.exibir_solicitacoes(solicitacoes)

    def exibir_solicitacoes(self, solicitacoes):
        """
        Exibe as solicitações de amizade na tela.

        Args:
            solicitacoes (list): Lista de solicitações no formato [{"username": str, "solicitacao": Solicitacao}, ...].
        """
        for widget in self.solicitacoes_frame.winfo_children():
            widget.destroy()  # Limpa o frame antes de adicionar novas solicitações

        if not solicitacoes:
            tk.Label(self.solicitacoes_frame, text="Nenhuma solicitação de amizade.", font=("Arial", 12)).pack()
            return

        for solicitacao_data in solicitacoes:
            username = solicitacao_data["username"]
            solicitacao = solicitacao_data["solicitacao"]

            frame = tk.Frame(self.solicitacoes_frame)
            frame.pack(pady=5, padx=10, fill="x")

            # Texto da solicitação
            tk.Label(frame, text=f"Solicitação de amizade de {username}", font=("Arial", 12)).pack(side="left", padx=5)

            # Botão de aceitar
            aceitar_button = tk.Button(frame, text="Aceitar", command=lambda s=solicitacao: self.aceitar_solicitacao(s))
            aceitar_button.pack(side="right", padx=5)

            # Botão de recusar
            recusar_button = tk.Button(frame, text="Recusar", command=lambda s=solicitacao: self.recusar_solicitacao(s))
            recusar_button.pack(side="right", padx=5)

    def aceitar_solicitacao(self, solicitacao):
        try:
            self.controller.aceitar(solicitacao)  # Chama o método do controlador
            messagebox.showinfo("Solicitação Aceita", f"Você aceitou a solicitação de {solicitacao.remetente.username}.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aceitar solicitação: {str(e)}")

    def recusar_solicitacao(self, solicitacao):
        try:
            self.controller.recusar(solicitacao)  # Chama o método do controlador
            messagebox.showinfo("Solicitação Recusada", f"Você recusou a solicitação de {solicitacao.remetente.username}.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao recusar solicitação: {str(e)}")


# aqui só exemplo de uso, tirar no final
if __name__ == "__main__":
    from models.user import User
    from models.solicitacao import Solicitacao
    from controllers.solicitacao_controller import SolicitacaoController

    class MockSolicitacaoController(SolicitacaoController):
        def aceitar(self, solicitacao):
            print(f"Aceitando solicitação de {solicitacao.remetente.username}")

        def recusar(self, solicitacao):
            print(f"Recusando solicitação de {solicitacao.remetente.username}")

    def voltar_para_perfil():
        messagebox.showinfo("Voltar", "Voltando para a tela de perfil do usuário.")
        root.destroy()
    
    # criando usuario ficticio
    user1 = User(
        cpf="12345678901",
        username="Joao",
        email="joao@example.com",
        birthdate=datetime.date(1990, 1, 1),  
        encrypted_password="123"
    )
    user2 = User(
        cpf="98765432100",
        username="Maria",
        email="maria@example.com",
        birthdate=datetime.date(1992, 2, 2),  
        encrypted_password="123"
    )
    
    # criando solicitacao ficticia
    solicitacoes_exemplo = [
        {"username": user1.username, "solicitacao": Solicitacao(destinatario=user2, remetente=user1)},
        {"username": user2.username, "solicitacao": Solicitacao(destinatario=user1, remetente=user2)},
    ]

    root = tk.Tk()
    controller = MockSolicitacaoController()
    app = SolicitacaoView(root, solicitacoes_exemplo, voltar_para_perfil, controller)
    root.geometry("1920x1080")
    root.mainloop()
    