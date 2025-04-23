import tkinter as tk
from tkinter import messagebox

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
        self.solicitacoes = list(solicitacoes)

        # Configurações da janela principal
        self.root.title("Amizades")
        self.root.geometry("600x600")  # Tamanho fixo
        self.root.resizable(False, False)  # Impede redimensionamento
        self.root.configure(bg="#f0f0f0")

        # Título da tela
        tk.Label(
            root, 
            text="Solicitações de Amizade", 
            font=("Arial", 20, "bold"), 
            bg="#f0f0f0", 
            fg="#333"
        ).pack(pady=20)

        # Botão de voltar
        tk.Button(
            root, 
            text="Voltar", 
            command=voltar_callback, 
            font=("Arial", 12, "bold"), 
            bg="#d3d3d3",  # Cinza
            fg="black", 
            relief="flat", 
            cursor="hand2", 
            width=10
        ).place(relx=0.85, rely=0.05)

        # Frame para exibir as solicitações
        self.solicitacoes_frame = tk.Frame(root, bg="#f0f0f0")
        self.solicitacoes_frame.pack(pady=20, fill="both", expand=True)

        self.exibir_solicitacoes()

        # Adicionando a logo no meio inferior
        self._adicionar_logo()

    def exibir_solicitacoes(self):
        for w in self.solicitacoes_frame.winfo_children():
            w.destroy()
    
        if not self.solicitacoes:
            tk.Label(
                self.solicitacoes_frame, 
                text="Nenhuma solicitação de amizade.", 
                font=("Arial", 14), 
                bg="#f0f0f0", 
                fg="#555"
            ).pack(pady=20)
            return
    
        for solicitacao in self.solicitacoes:
            self._criar_frame_solicitacao(self.solicitacoes_frame, solicitacao)

    def _criar_frame_solicitacao(self, parent, solicitacao):
        frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
        frame.pack(pady=10, padx=20, fill="x")

        remetente = solicitacao.remetente.username
        tk.Label(
            frame, 
            text=f"Solicitação de amizade de {remetente}", 
            font=("Arial", 12), 
            bg="white", 
            fg="#333"
        ).pack(side="left", padx=10)

        tk.Button(
            frame,
            text="Aceitar",
            command=lambda: self._processar_solicitacao(solicitacao, True),
            font=("Arial", 10, "bold"),
            bg="#d3d3d3",  # Cinza
            fg="black",
            relief="flat",
            cursor="hand2",
            width=8
        ).pack(side="right", padx=5)

        tk.Button(
            frame,
            text="Recusar",
            command=lambda: self._processar_solicitacao(solicitacao, False),
            font=("Arial", 10, "bold"),
            bg="#d3d3d3",  # Cinza
            fg="black",
            relief="flat",
            cursor="hand2",
            width=8
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
            self.solicitacoes.remove(solicitacao)
            self.exibir_solicitacoes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar solicitação: {e}")

    def _adicionar_logo(self):
        # Carregando a imagem da logo no formato PNG ou GIF
        try:
            # Certifique-se de que a imagem está no formato PNG ou GIF
            import os
            logo_path = os.path.join(os.path.dirname(__file__), "../images/logo.png")
            photo = tk.PhotoImage(file=logo_path)
    
            # Adicionando a imagem no meio inferior
            logo_label = tk.Label(self.root, image=photo, bg="#f0f0f0")
            logo_label.image = photo  # Referência para evitar garbage collection
            logo_label.pack(side="bottom", pady=20)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar a logo: {e}")
