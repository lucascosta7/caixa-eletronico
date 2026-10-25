
import customtkinter as ctk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation

from services.contas import autenticar_conta, cadastrar_conta
from services.operacoes import (
    consultar_saldo,
    depositar,
    sacar,
    transferir,
    consultar_extrato,
)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CaixaEletronicoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Banco Digital | Caixa Eletrônico")
        self.geometry("1000x650")
        self.minsize(800, 550)
        self.configure(fg_color="#F3F6FC")

        self.conta_atual = None
        self.conteudo = None
        self.rotulo_saldo = None
        self.campo_conta = None
        self.campo_senha = None

        self.criar_cabecalho()
        self.mostrar_login()

    # --------------------------------------------------
    # ESTRUTURA PRINCIPAL
    # --------------------------------------------------

    def criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self,
            fg_color="#102A43",
            corner_radius=0,
            height=65,
        )
        cabecalho.pack(fill="x")
        cabecalho.pack_propagate(False)

        ctk.CTkLabel(
            cabecalho,
            text="BANCO DIGITAL",
            font=("Segoe UI", 23, "bold"),
            text_color="#FFFFFF",
        ).pack(side="left", padx=30)

        ctk.CTkLabel(
            cabecalho,
            text="CAIXA ELETRÔNICO",
            font=("Segoe UI", 12),
            text_color="#88D4F8",
        ).pack(side="right", padx=30)

    def limpar_tela(self):
        if self.conteudo is not None:
            self.conteudo.destroy()

        self.conteudo = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.conteudo.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30,
        )

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    def mostrar_login(self):
        self.conta_atual = None
        self.rotulo_saldo = None

        self.limpar_tela()

        ctk.CTkLabel(
            self.conteudo,
            text="Acesse sua conta",
            font=("Segoe UI", 28, "bold"),
            text_color="#102A43",
        ).pack(pady=(45, 8))

        ctk.CTkLabel(
            self.conteudo,
            text="Informe seus dados para continuar.",
            font=("Segoe UI", 14),
            text_color="#52667A",
        ).pack(pady=(0, 25))

        self.campo_conta = ctk.CTkEntry(
            self.conteudo,
            width=320,
            height=45,
            placeholder_text="Número da conta",
        )
        self.campo_conta.pack(pady=8)

        self.campo_senha = ctk.CTkEntry(
            self.conteudo,
            width=320,
            height=45,
            placeholder_text="Senha",
            show="*",
        )
        self.campo_senha.pack(pady=8)

        self.campo_senha.bind(
            "<Return>",
            lambda evento: self.fazer_login(),
        )

        ctk.CTkButton(
            self.conteudo,
            text="Entrar",
            width=320,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color="#1769AA",
            hover_color="#12558A",
            command=self.fazer_login,
        ).pack(pady=(20, 8))

        ctk.CTkButton(
            self.conteudo,
            text="Criar minha conta",
            width=320,
            height=42,
            font=("Segoe UI", 14, "bold"),
            fg_color="transparent",
            text_color="#1769AA",
            hover_color="#DCEAF7",
            border_width=1,
            border_color="#1769AA",
            command=self.mostrar_cadastro,
        ).pack(pady=(0, 15))

        ctk.CTkLabel(
            self,
            text="© 2026 Banco Digital",
            font=("Segoe UI", 11),
            text_color="#718096",
        ).pack(pady=(0, 12))

    def fazer_login(self):
        numero = self.campo_conta.get().strip()
        senha = self.campo_senha.get()

        if not numero or not senha:
            messagebox.showwarning(
                "Atenção",
                "Informe o número da conta e a senha.",
                parent=self,
            )
            return

        try:
            conta = autenticar_conta(numero, senha)

            if conta is None:
                messagebox.showerror(
                    "Falha no login",
                    "Conta ou senha inválida, ou conta bloqueada.",
                    parent=self,
                )
                return

            self.conta_atual = conta
            self.mostrar_painel()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível entrar:\n{erro}",
                parent=self,
            )

    # --------------------------------------------------
    # CADASTRO DE CLIENTES
    # --------------------------------------------------

    def mostrar_cadastro(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Criar conta bancária")
        janela.geometry("460x570")
        janela.resizable(False, False)
        janela.transient(self)
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Abra sua conta",
            font=("Segoe UI", 25, "bold"),
            text_color="#102A43",
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            janela,
            text="Preencha os dados para se cadastrar.",
            font=("Segoe UI", 13),
            text_color="#52667A",
        ).pack(pady=(0, 20))

        campo_nome = ctk.CTkEntry(
            janela,
            width=340,
            height=42,
            placeholder_text="Nome completo",
        )
        campo_nome.pack(pady=8)

        campo_senha = ctk.CTkEntry(
            janela,
            width=340,
            height=42,
            placeholder_text="Crie uma senha (mínimo 8 caracteres)",
            show="*",
        )
        campo_senha.pack(pady=8)

        campo_confirmacao = ctk.CTkEntry(
            janela,
            width=340,
            height=42,
            placeholder_text="Confirme sua senha",
            show="*",
        )
        campo_confirmacao.pack(pady=8)

        campo_deposito = ctk.CTkEntry(
            janela,
            width=340,
            height=42,
            placeholder_text="Depósito inicial (opcional)",
        )
        campo_deposito.pack(pady=8)

        ctk.CTkLabel(
            janela,
            text="Deixe o depósito vazio para começar com R$ 0,00.",
            font=("Segoe UI", 11),
            text_color="#52667A",
        ).pack(pady=(0, 5))

        def cadastrar():
            nome = campo_nome.get().strip()
            senha = campo_senha.get()
            confirmacao = campo_confirmacao.get()
            deposito_texto = campo_deposito.get().strip()

            if not nome:
                messagebox.showwarning(
                    "Cadastro",
                    "Informe o nome do titular.",
                    parent=janela,
                )
                return

            if len(senha) < 8:
                messagebox.showwarning(
                    "Cadastro",
                    "A senha deve ter pelo menos 8 caracteres.",
                    parent=janela,
                )
                return

            if senha != confirmacao:
                messagebox.showwarning(
                    "Cadastro",
                    "As senhas não coincidem.",
                    parent=janela,
                )
                return

            try:
                deposito_centavos = (
                    self.converter_para_centavos(deposito_texto)
                    if deposito_texto
                    else 0
                )

                if deposito_centavos < 0:
                    raise ValueError(
                        "O depósito inicial não pode ser negativo."
                    )

                conta = cadastrar_conta(
                    titular=nome,
                    senha=senha,
                    deposito_inicial=deposito_centavos,
                )

                messagebox.showinfo(
                    "Conta criada com sucesso!",
                    f"Bem-vindo(a), {conta['titular']}!\n\n"
                    f"Número da conta: {conta['numero']}\n"
                    f"Saldo inicial: "
                    f"{self.formatar_dinheiro(conta['saldo_centavos'])}\n\n"
                    "Guarde o número da conta para entrar.",
                    parent=janela,
                )

                janela.destroy()

                self.campo_conta.delete(0, "end")
                self.campo_conta.insert(0, conta["numero"])
                self.campo_senha.delete(0, "end")

            except ValueError as erro:
                messagebox.showwarning(
                    "Não foi possível cadastrar",
                    str(erro),
                    parent=janela,
                )

            except Exception as erro:
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível criar a conta:\n{erro}",
                    parent=janela,
                )

        ctk.CTkButton(
            janela,
            text="Criar conta bancária",
            width=340,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color="#1769AA",
            hover_color="#12558A",
            command=cadastrar,
        ).pack(pady=(15, 8))

        ctk.CTkButton(
            janela,
            text="Cancelar",
            width=340,
            height=38,
            fg_color="transparent",
            text_color="#52667A",
            hover_color="#E5EAF1",
            command=janela.destroy,
        ).pack(pady=(0, 15))

    # --------------------------------------------------
    # PAINEL PRINCIPAL
    # --------------------------------------------------

    def mostrar_painel(self):
        self.rotulo_saldo = None
        self.limpar_tela()

        ctk.CTkLabel(
            self.conteudo,
            text=f"Olá, {self.conta_atual['titular']}!",
            font=("Segoe UI", 27, "bold"),
            text_color="#102A43",
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.conteudo,
            text=f"Conta: {self.conta_atual['numero']}",
            font=("Segoe UI", 13),
            text_color="#52667A",
        ).pack(anchor="w", pady=(4, 20))

        cartao_saldo = ctk.CTkFrame(
            self.conteudo,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#DCE5F0",
        )
        cartao_saldo.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            cartao_saldo,
            text="SALDO DISPONÍVEL",
            font=("Segoe UI", 12, "bold"),
            text_color="#52667A",
        ).pack(anchor="w", padx=24, pady=(16, 3))

        self.rotulo_saldo = ctk.CTkLabel(
            cartao_saldo,
            text="Carregando...",
            font=("Segoe UI", 30, "bold"),
            text_color="#102A43",
        )
        self.rotulo_saldo.pack(anchor="w", padx=24, pady=(0, 16))

        operacoes = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent",
        )
        operacoes.pack(fill="x")

        for coluna in range(2):
            operacoes.grid_columnconfigure(
                coluna,
                weight=1,
                uniform="operacao",
            )

        botoes = [
            ("Consultar saldo", self.atualizar_saldo, 0, 0),
            ("Realizar saque", self.abrir_saque, 0, 1),
            ("Depositar dinheiro", self.abrir_deposito, 1, 0),
            ("Transferir valores", self.abrir_transferencia, 1, 1),
            ("Consultar extrato", self.mostrar_extrato, 2, 0),
            ("Sair da conta", self.mostrar_login, 2, 1),
        ]

        for texto, comando, linha, coluna in botoes:
            ctk.CTkButton(
                operacoes,
                text=texto,
                height=48,
                corner_radius=9,
                font=("Segoe UI", 14, "bold"),
                fg_color="#1769AA",
                hover_color="#12558A",
                command=comando,
            ).grid(
                row=linha,
                column=coluna,
                padx=7,
                pady=7,
                sticky="ew",
            )

        ctk.CTkLabel(
            self,
            text="© 2026 Banco Digital",
            font=("Segoe UI", 11),
            text_color="#718096",
        ).pack(pady=(0, 10))

        self.atualizar_saldo()

    # --------------------------------------------------
    # UTILITÁRIOS
    # --------------------------------------------------

    @staticmethod
    def formatar_dinheiro(centavos):
        valor = Decimal(centavos) / Decimal(100)

        return (
            "R$ "
            + f"{valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    @staticmethod
    def converter_para_centavos(entrada):
        try:
            valor = Decimal(entrada.strip().replace(",", "."))
        except (InvalidOperation, AttributeError):
            raise ValueError("Informe um valor monetário válido.")

        if not valor.is_finite():
            raise ValueError("Informe um valor monetário válido.")

        centavos = valor * 100

        if centavos != centavos.to_integral_value():
            raise ValueError("Informe no máximo duas casas decimais.")

        return int(centavos)

    def pedir_valor(self, titulo, instrucao):
        dialogo = ctk.CTkInputDialog(
            title=titulo,
            text=instrucao,
        )

        entrada = dialogo.get_input()

        if entrada is None:
            return None

        valor = self.converter_para_centavos(entrada)

        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        return valor

    # --------------------------------------------------
    # CONSULTA DE SALDO
    # --------------------------------------------------

    def atualizar_saldo(self):
        if self.conta_atual is None or self.rotulo_saldo is None:
            return

        try:
            saldo = consultar_saldo(self.conta_atual["id"])

            self.rotulo_saldo.configure(
                text=self.formatar_dinheiro(saldo)
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao consultar saldo",
                str(erro),
                parent=self,
            )

    # --------------------------------------------------
    # DEPÓSITO
    # --------------------------------------------------

    def abrir_deposito(self):
        try:
            valor = self.pedir_valor(
                "Depósito",
                "Digite o valor a depositar (ex.: 50,00):",
            )

            if valor is None:
                return

            saldo = depositar(
                self.conta_atual["id"],
                valor,
            )

            self.atualizar_saldo()

            messagebox.showinfo(
                "Depósito realizado",
                "Depósito realizado com sucesso!\n"
                f"Saldo atual: {self.formatar_dinheiro(saldo)}",
                parent=self,
            )

        except ValueError as erro:
            messagebox.showwarning(
                "Depósito não realizado",
                str(erro),
                parent=self,
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self,
            )

    # --------------------------------------------------
    # SAQUE
    # --------------------------------------------------

    def abrir_saque(self):
        try:
            valor = self.pedir_valor(
                "Saque",
                "Digite o valor a sacar (ex.: 50,00):",
            )

            if valor is None:
                return

            saldo = sacar(
                self.conta_atual["id"],
                valor,
            )

            self.atualizar_saldo()

            messagebox.showinfo(
                "Saque realizado",
                "Saque realizado com sucesso!\n"
                f"Saldo atual: {self.formatar_dinheiro(saldo)}",
                parent=self,
            )

        except ValueError as erro:
            messagebox.showwarning(
                "Saque não realizado",
                str(erro),
                parent=self,
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self,
            )

    # --------------------------------------------------
    # TRANSFERÊNCIA
    # --------------------------------------------------

    def abrir_transferencia(self):
        numero_destino = ctk.CTkInputDialog(
            title="Transferência",
            text="Número da conta de destino:",
        ).get_input()

        if numero_destino is None:
            return

        numero_destino = numero_destino.strip()

        if not numero_destino:
            messagebox.showwarning(
                "Transferência",
                "Informe a conta de destino.",
                parent=self,
            )
            return

        try:
            valor = self.pedir_valor(
                "Transferência",
                "Digite o valor a transferir (ex.: 50,00):",
            )

            if valor is None:
                return

            saldo = transferir(
                self.conta_atual["id"],
                numero_destino,
                valor,
            )

            self.atualizar_saldo()

            messagebox.showinfo(
                "Transferência realizada",
                "Transferência realizada com sucesso!\n"
                f"Saldo atual: {self.formatar_dinheiro(saldo)}",
                parent=self,
            )

        except ValueError as erro:
            messagebox.showwarning(
                "Transferência não realizada",
                str(erro),
                parent=self,
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self,
            )

    # --------------------------------------------------
    # EXTRATO
    # --------------------------------------------------

    def mostrar_extrato(self):
        try:
            transacoes = consultar_extrato(
                self.conta_atual["id"]
            )

            janela = ctk.CTkToplevel(self)
            janela.title("Extrato bancário")
            janela.geometry("750x450")
            janela.minsize(550, 300)
            janela.transient(self)

            ctk.CTkLabel(
                janela,
                text="Extrato bancário",
                font=("Segoe UI", 24, "bold"),
                text_color="#102A43",
            ).pack(anchor="w", padx=20, pady=(20, 10))

            lista = ctk.CTkScrollableFrame(
                janela,
                fg_color="#FFFFFF",
            )
            lista.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=(0, 20),
            )

            if not transacoes:
                ctk.CTkLabel(
                    lista,
                    text="Nenhuma movimentação encontrada.",
                    text_color="#52667A",
                ).pack(pady=20)
                return

            for transacao in transacoes:
                linha = ctk.CTkFrame(
                    lista,
                    fg_color="#F3F6FC",
                    corner_radius=8,
                )
                linha.pack(fill="x", padx=5, pady=5)

                valor = self.formatar_dinheiro(
                    transacao["valor_centavos"]
                )

                descricao = (
                    f"{transacao['tipo']} — "
                    f"{transacao['direcao']}\n"
                    f"{transacao['data_hora']}"
                )

                ctk.CTkLabel(
                    linha,
                    text=descricao,
                    justify="left",
                    font=("Segoe UI", 12),
                    text_color="#102A43",
                ).pack(side="left", padx=12, pady=12)

                ctk.CTkLabel(
                    linha,
                    text=valor,
                    font=("Segoe UI", 14, "bold"),
                    text_color="#1769AA",
                ).pack(side="right", padx=12)

        except Exception as erro:
            messagebox.showerror(
                "Erro no extrato",
                str(erro),
                parent=self,
            )


if __name__ == "__main__":
    app = CaixaEletronicoApp()
    app.mainloop()