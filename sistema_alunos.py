# Tarefa 02 - Sistema de Cadastro de Alunos
# Disciplina: Introdução à Ciência da Computação
# Aluno(s): Nome 1 (matrícula), Nome 2 (matrícula)
# Data: 24/11/2026

import sys
from datetime import datetime


class CadastroAlunos:
    def __init__(self):
        self.alunos = []

    @staticmethod
    def validar_dados(matricula, nome, endereco, data_nasc):
        dados = {
            "matricula": matricula.strip(),
            "nome": nome.strip(),
            "endereco": endereco.strip(),
            "data_nasc": data_nasc.strip(),
        }
        if any(not valor for valor in dados.values()):
            raise ValueError("Todos os campos são obrigatórios.")
        try:
            data = datetime.strptime(dados["data_nasc"], "%d/%m/%Y")
        except ValueError:
            raise ValueError("Data inválida. Informe no formato dd/mm/aaaa.")
        if data.strftime("%d/%m/%Y") != dados["data_nasc"]:
            raise ValueError("Data inválida. Informe no formato dd/mm/aaaa.")
        return dados

    def cadastrar(self, matricula, nome, endereco, data_nasc):
        aluno = self.validar_dados(matricula, nome, endereco, data_nasc)
        if self.buscar_matricula(aluno["matricula"]):
            raise ValueError("Já existe um aluno com essa matrícula.")
        self.alunos.append(aluno)
        return aluno

    def buscar_matricula(self, matricula):
        chave = matricula.strip().casefold()
        return next(
            (aluno for aluno in self.alunos
             if aluno["matricula"].casefold() == chave),
            None,
        )

    def buscar(self, termo):
        chave = termo.strip().casefold()
        if not chave:
            return []
        return [
            aluno for aluno in self.alunos
            if chave in aluno["matricula"].casefold()
            or chave in aluno["nome"].casefold()
        ]

    def alterar(self, matricula_atual, matricula, nome, endereco, data_nasc):
        aluno_atual = self.buscar_matricula(matricula_atual)
        if aluno_atual is None:
            raise ValueError("Aluno não encontrado.")
        dados = self.validar_dados(matricula, nome, endereco, data_nasc)
        existente = self.buscar_matricula(dados["matricula"])
        if existente is not None and existente is not aluno_atual:
            raise ValueError("Já existe um aluno com essa matrícula.")
        aluno_atual.update(dados)
        return aluno_atual

    def excluir(self, matricula):
        aluno = self.buscar_matricula(matricula)
        if aluno is None:
            raise ValueError("Aluno não encontrado.")
        self.alunos.remove(aluno)
        return aluno


def exibir_alunos(alunos):
    if not alunos:
        print("Nenhum aluno encontrado.")
        return
    for aluno in alunos:
        print(
            f"Matrícula: {aluno['matricula']} | Nome: {aluno['nome']} | "
            f"Endereço: {aluno['endereco']} | "
            f"Data de Nascimento: {aluno['data_nasc']}"
        )


def executar_terminal(cadastro):
    while True:
        print("\n=== Sistema de Cadastro de Alunos ===")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Buscar")
        print("4 - Alterar")
        print("5 - Excluir")
        print("0 - Sair")
        opcao = input("Digite a opção: ").strip()

        try:
            if opcao == "1":
                print("\n=== Cadastrar Aluno ===")
                cadastro.cadastrar(
                    input("Matrícula: "),
                    input("Nome: "),
                    input("Endereço: "),
                    input("Data de Nascimento: "),
                )
                print("Aluno cadastrado com sucesso!")
            elif opcao == "2":
                print("\n=== Alunos Cadastrados ===")
                exibir_alunos(cadastro.alunos)
            elif opcao == "3":
                termo = input("Digite o nome ou matrícula: ")
                exibir_alunos(cadastro.buscar(termo))
            elif opcao == "4":
                matricula = input("Matrícula do aluno que deseja alterar: ")
                aluno = cadastro.buscar_matricula(matricula)
                if aluno is None:
                    print("Aluno não encontrado.")
                    continue
                print("Deixe um campo em branco para manter o valor atual.")
                valores = {}
                for campo, rotulo in (
                    ("matricula", "Matrícula"),
                    ("nome", "Nome"),
                    ("endereco", "Endereço"),
                    ("data_nasc", "Data de Nascimento"),
                ):
                    informado = input(f"{rotulo} [{aluno[campo]}]: ").strip()
                    valores[campo] = informado or aluno[campo]
                cadastro.alterar(matricula, **valores)
                print("Dados do aluno alterados com sucesso!")
            elif opcao == "5":
                matricula = input("Matrícula do aluno que deseja excluir: ")
                aluno = cadastro.buscar_matricula(matricula)
                if aluno is None:
                    print("Aluno não encontrado.")
                    continue
                confirmacao = input(
                    f"Confirma a exclusão de {aluno['nome']}? (s/n): "
                ).strip().casefold()
                if confirmacao == "s":
                    cadastro.excluir(matricula)
                    print("Aluno excluído com sucesso.")
                else:
                    print("Exclusão cancelada.")
            elif opcao == "0":
                print("Programa encerrado.")
                break
            else:
                print("Opção inválida. Escolha uma opção do menu.")
        except ValueError as erro:
            print(f"Erro: {erro}")


def executar_grafico(cadastro):
    import tkinter as tk
    from tkinter import messagebox, ttk

    azul_fundo = "#0B1730"
    azul_painel = "#142746"
    azul_botao = "#2878D0"
    azul_claro = "#DCEBFA"
    laranja = "#E69A22"
    vermelho = "#D94B55"
    branco = "#F5F8FC"

    def arredondado(canvas, x1, y1, x2, y2, raio, cor):
        pontos = [
            x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
            x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
            x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1,
        ]
        return canvas.create_polygon(
            pontos, smooth=True, splinesteps=24, fill=cor, outline=cor
        )

    class BotaoArredondado(tk.Canvas):
        def __init__(self, master, texto, comando, cor, largura=150):
            super().__init__(
                master, width=largura, height=42, bg=master["bg"],
                highlightthickness=0, cursor="hand2",
            )
            self.comando = comando
            self.cor = cor
            self.fundo = arredondado(self, 2, 2, largura - 2, 40, 13, cor)
            self.etiqueta = self.create_text(
                largura // 2, 21, text=texto, fill="white",
                font=("Segoe UI", 10, "bold"),
            )
            self.bind("<Button-1>", self._clicar)
            self.bind("<Enter>", self._entrar)
            self.bind("<Leave>", self._sair)

        def _clicar(self, _evento):
            self.comando()

        def _entrar(self, _evento):
            self.itemconfigure(self.fundo, fill="#3B8CE0")

        def _sair(self, _evento):
            self.itemconfigure(self.fundo, fill=self.cor)

    class CampoArredondado(tk.Frame):
        def __init__(self, master, largura=420):
            super().__init__(master, bg=master["bg"])
            canvas = tk.Canvas(
                self, width=largura, height=40, bg=master["bg"],
                highlightthickness=0,
            )
            canvas.pack()
            arredondado(canvas, 1, 1, largura - 1, 39, 12, azul_claro)
            self.entrada = tk.Entry(
                canvas, bd=0, relief="flat", bg=azul_claro, fg="#16263B",
                insertbackground="#16263B", font=("Segoe UI", 10),
            )
            canvas.create_window(
                14, 20, anchor="w", width=largura - 28, height=26,
                window=self.entrada,
            )

        def get(self):
            return self.entrada.get()

        def set(self, valor):
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, valor)

        def limpar(self):
            self.entrada.delete(0, tk.END)

    raiz = tk.Tk()
    raiz.title("Sistema de Cadastro de Alunos")
    raiz.geometry("1040x720")
    raiz.minsize(900, 650)
    raiz.configure(bg=azul_fundo)

    tk.Label(
        raiz, text="Sistema de Cadastro de Alunos", bg=azul_fundo,
        fg=branco, font=("Segoe UI", 23, "bold"),
    ).pack(anchor="w", padx=32, pady=(24, 2))
    tk.Label(
        raiz, text="Gerencie os dados dos alunos em um só lugar",
        bg=azul_fundo, fg="#AFC2DC", font=("Segoe UI", 10),
    ).pack(anchor="w", padx=34, pady=(0, 18))

    painel = tk.Frame(raiz, bg=azul_painel, padx=22, pady=18)
    painel.pack(fill="x", padx=30, pady=(0, 16))
    tk.Label(
        painel, text="Dados do aluno", bg=azul_painel, fg=branco,
        font=("Segoe UI", 14, "bold"),
    ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

    campos = {}
    definicoes = [
        ("matricula", "Matrícula", 0, 0),
        ("nome", "Nome", 0, 2),
        ("endereco", "Endereço", 1, 0),
        ("data_nasc", "Data de Nascimento (dd/mm/aaaa)", 1, 2),
    ]
    for chave, rotulo, linha, coluna in definicoes:
        tk.Label(
            painel, text=rotulo, bg=azul_painel, fg="#C8D7E9",
            font=("Segoe UI", 9),
        ).grid(row=linha * 2 + 1, column=coluna, sticky="w",
               padx=(0, 12), pady=(2, 4))
        campo = CampoArredondado(painel, largura=440)
        campo.grid(row=linha * 2 + 2, column=coluna, sticky="w",
                   padx=(0, 16), pady=(0, 8))
        campos[chave] = campo

    selecionado = {"matricula": None}

    acoes = tk.Frame(painel, bg=azul_painel)
    acoes.grid(row=5, column=0, columnspan=4, sticky="w", pady=(8, 0))

    busca = tk.Frame(raiz, bg=azul_fundo)
    busca.pack(fill="x", padx=30, pady=(0, 10))
    tk.Label(
        busca, text="Buscar por nome ou matrícula", bg=azul_fundo,
        fg="#C8D7E9", font=("Segoe UI", 10),
    ).pack(side="left", padx=(0, 12))
    campo_busca = CampoArredondado(busca, largura=350)
    campo_busca.pack(side="left", padx=(0, 12))

    area_lista = tk.Frame(raiz, bg=azul_painel, padx=14, pady=14)
    area_lista.pack(fill="both", expand=True, padx=30, pady=(0, 24))
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure(
        "Treeview", background="#F4F7FB", foreground="#17273D",
        fieldbackground="#F4F7FB", rowheight=30, font=("Segoe UI", 9),
    )
    estilo.configure(
        "Treeview.Heading", background="#D5E5F6", foreground="#142746",
        font=("Segoe UI", 9, "bold"),
    )
    estilo.map("Treeview", background=[("selected", "#2878D0")],
               foreground=[("selected", "white")])
    tabela = ttk.Treeview(
        area_lista, columns=("matricula", "nome", "endereco", "data_nasc"),
        show="headings", selectmode="browse",
    )
    for coluna, titulo, largura in (
        ("matricula", "Matrícula", 130),
        ("nome", "Nome", 210),
        ("endereco", "Endereço", 390),
        ("data_nasc", "Data de Nascimento", 170),
    ):
        tabela.heading(coluna, text=titulo)
        tabela.column(coluna, width=largura, anchor="w")
    barra = ttk.Scrollbar(area_lista, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=barra.set)
    tabela.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    def atualizar_tabela(alunos=None):
        for item in tabela.get_children():
            tabela.delete(item)
        for aluno in cadastro.alunos if alunos is None else alunos:
            tabela.insert(
                "", "end",
                values=(
                    aluno["matricula"], aluno["nome"], aluno["endereco"],
                    aluno["data_nasc"],
                ),
            )

    def limpar_formulario():
        for campo in campos.values():
            campo.limpar()
        selecionado["matricula"] = None
        tabela.selection_remove(tabela.selection())

    def cadastrar():
        try:
            cadastro.cadastrar(*(campos[chave].get() for chave in (
                "matricula", "nome", "endereco", "data_nasc"
            )))
        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=raiz)
            return
        atualizar_tabela()
        limpar_formulario()
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!",
                            parent=raiz)

    def alterar():
        matricula_atual = selecionado["matricula"]
        if matricula_atual is None:
            messagebox.showwarning(
                "Atenção", "Selecione um aluno na lista para alterar.",
                parent=raiz,
            )
            return
        try:
            cadastro.alterar(
                matricula_atual,
                *(campos[chave].get() for chave in (
                    "matricula", "nome", "endereco", "data_nasc"
                )),
            )
        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=raiz)
            return
        atualizar_tabela()
        limpar_formulario()
        messagebox.showinfo("Sucesso", "Dados alterados com sucesso!",
                            parent=raiz)

    def excluir():
        matricula = selecionado["matricula"]
        if matricula is None:
            messagebox.showwarning(
                "Atenção", "Selecione um aluno na lista para excluir.",
                parent=raiz,
            )
            return
        aluno = cadastro.buscar_matricula(matricula)
        if aluno and messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir o cadastro de {aluno['nome']}?",
            parent=raiz,
        ):
            cadastro.excluir(matricula)
            atualizar_tabela()
            limpar_formulario()
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso.",
                                parent=raiz)

    def pesquisar():
        termo = campo_busca.get()
        atualizar_tabela(cadastro.buscar(termo) if termo.strip()
                         else cadastro.alunos)

    def selecionar_aluno(_evento):
        itens = tabela.selection()
        if not itens:
            return
        valores = tabela.item(itens[0], "values")
        selecionado["matricula"] = valores[0]
        for chave, valor in zip(
            ("matricula", "nome", "endereco", "data_nasc"), valores
        ):
            campos[chave].set(valor)

    BotaoArredondado(
        acoes, "Cadastrar aluno", cadastrar, azul_botao, 155
    ).pack(side="left", padx=(0, 10))
    BotaoArredondado(
        acoes, "Salvar alteração", alterar, laranja, 165
    ).pack(side="left", padx=(0, 10))
    BotaoArredondado(
        acoes, "Excluir selecionado", excluir, vermelho, 175
    ).pack(side="left", padx=(0, 10))
    BotaoArredondado(
        acoes, "Limpar campos", limpar_formulario, "#456789", 145
    ).pack(side="left")
    BotaoArredondado(
        busca, "Buscar", pesquisar, azul_botao, 105
    ).pack(side="left", padx=(0, 8))
    BotaoArredondado(
        busca, "Listar todos", atualizar_tabela, "#456789", 125
    ).pack(side="left")
    tabela.bind("<<TreeviewSelect>>", selecionar_aluno)
    atualizar_tabela()
    raiz.mainloop()


if __name__ == "__main__":
    dados = CadastroAlunos()
    if "--terminal" in sys.argv:
        executar_terminal(dados)
    else:
        executar_grafico(dados)
