import tkinter as tk
from tkinter import messagebox
import datetime

class SolicitacaoView:
    def __init__(self, root, solicitacoes, voltar_callback, controller):
        """
        Args:
            root (tk.Tk)
            solicitacoes (list[Solicitacao])
            voltar_callback (callable)
            controller (SolicitacaoController)
        """
        self.root = root
        self.controller = controller
        # agora guardamos a lista de Solicitacao
        self.solicitacoes = list(solicitacoes)

        self.root.title("Amizades")
        tk.Label(root, text="Amizades", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(root, text="Voltar", command=voltar_callback).place(relx=0.9, rely=0.05)

        self.solicitacoes_frame = tk.Frame(root)
        self.solicitacoes_frame.pack(pady=20)

        self.exibir_solicitacoes()

    def exibir_solicitacoes(self):
        # limpa tudo
        for w in self.solicitacoes_frame.winfo_children():
            w.destroy()

        if not self.solicitacoes:
            tk.Label(self.solicitacoes_frame, text="Nenhuma solicitação de amizade.", font=("Arial", 12)).pack()
            return

        for solicitacao in list(self.solicitacoes):
            frame = tk.Frame(self.solicitacoes_frame)
            frame.pack(pady=5, padx=10, fill="x")

            remetente = solicitacao.remetente.username
            tk.Label(frame, text=f"Solicitação de amizade de {remetente}", font=("Arial", 12)) \
                .pack(side="left", padx=5)

            tk.Button(
                frame,
                text="Aceitar",
                command=lambda s=solicitacao: self._processar_solicitacao(s, True)
            ).pack(side="right", padx=5)

            tk.Button(
                frame,
                text="Recusar",
                command=lambda s=solicitacao: self._processar_solicitacao(s, False)
            ).pack(side="right", padx=5)

    def _processar_solicitacao(self, solicitacao, aceitar: bool):
        try:
            if aceitar:
                self.controller.aceitar(solicitacao)
                msg = f"Você aceitou a solicitação de {solicitacao.remetente.username}."
            else:
                self.controller.recusar(solicitacao)
                msg = f"Você recusou a solicitação de {solicitacao.remetente.username}."
            messagebox.showinfo(
                "Solicitação " + ("Aceita" if aceitar else "Recusada"),
                msg
            )
            # remove da lista e re-renderiza
            self.solicitacoes.remove(solicitacao)
            self.exibir_solicitacoes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar solicitação: {e}")


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
    