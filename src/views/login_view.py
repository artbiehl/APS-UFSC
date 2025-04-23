# login_view.py
import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController
from repositories.user_repository import UserRepository

class LoginView:
    def __init__(self, root, controller: UserController, on_success):

        self.root = root
        self.controller = controller
        self.on_success = on_success

        root.title("Login")
        root.geometry("300x200")

        # Frame principal
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(expand=True)

        # Username
        tk.Label(frame, text="Usuário:", anchor="w").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Password
        tk.Label(frame, text="Senha:", anchor="w").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Botões
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Entrar", width=10, command=self._attempt_login).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar", width=10, command=root.destroy).pack(side="right", padx=5)

    def _attempt_login(self):
        user = self.username_entry.get().strip()
        pwd  = self.password_entry.get().strip()
        try:
            result = self.controller.login(user, pwd)
            messagebox.showinfo("Sucesso", f"Bem-vindo, {result['username']}!")
            self.on_success(result)
        except Exception as e:
            messagebox.showerror("Erro no login", str(e))
