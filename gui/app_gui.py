import tkinter as tk
from tkinter import ttk, messagebox

from dominio.usuario import Participante
from dominio.evento import Evento, Categoria
from dominio.ingresso import IngressoInteira, IngressoMeia, IngressoVIP
from dominio.gerenciador import GerenciadorDeEventos


class SistemaEventosGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema de Gestão de Eventos e Ingressos")
        self.root.geometry("680x500")
        self.root.resizable(False, False)

        # Instancia a mesma lógica de domínio da Sprint 2
        self.gerenciador = GerenciadorDeEventos()
        self._carregar_dados_iniciais()

        self._criar_widgets()
        self._atualizar_listas()

    def _carregar_dados_iniciais(self):
        cat_tech = Categoria("Tecnologia")
        cat_arte = Categoria("Cultura")

        ev1 = Evento("Tech Conference 2026", 2, cat_tech)
        ev1.adicionar_sessao("15/11/2026 14:00", "Auditório Central")

        ev2 = Evento("Festival de Jazz", 50, cat_arte)
        ev2.adicionar_sessao("20/11/2026 20:00", "Teatro Municipal")

        self.gerenciador.cadastrar_evento(ev1)
        self.gerenciador.cadastrar_evento(ev2)

    def _criar_widgets(self):
        # Sistema de Abas (Notebook)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- ABA 1: EVENTOS ---
        aba_eventos = ttk.Frame(notebook)
        notebook.add(aba_eventos, text="Eventos Disponíveis")

        ttk.Label(aba_eventos, text="Lista de Eventos e Lotação:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self.lista_eventos = tk.Listbox(aba_eventos, height=15, font=("Courier", 10))
        self.lista_eventos.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Button(aba_eventos, text="Atualizar Lista", command=self._atualizar_listas).pack(pady=10)

        # --- ABA 2: CADASTRAR PARTICIPANTE ---
        aba_participante = ttk.Frame(notebook)
        notebook.add(aba_participante, text="Cadastrar Participante")

        frame_form = ttk.Frame(aba_participante, padding=20)
        frame_form.pack(fill="x")

        ttk.Label(frame_form, text="Nome Completo:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = ttk.Entry(frame_form, width=45)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame_form, text="E-mail:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(frame_form, width=45)
        self.entry_email.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame_form, text="CPF:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_cpf = ttk.Entry(frame_form, width=45)
        self.entry_cpf.grid(row=2, column=1, pady=5, padx=10)

        ttk.Button(frame_form, text="Salvar Participante", command=self._cadastrar_participante).grid(row=3, column=1, sticky="e", pady=15)

        # --- ABA 3: COMPRAR INGRESSO ---
        aba_compra = ttk.Frame(notebook)
        notebook.add(aba_compra, text="Comprar Ingresso")

        frame_compra = ttk.Frame(aba_compra, padding=20)
        frame_compra.pack(fill="x")

        ttk.Label(frame_compra, text="Selecione o Participante:").grid(row=0, column=0, sticky="w", pady=8)
        self.combo_participante = ttk.Combobox(frame_compra, state="readonly", width=42)
        self.combo_participante.grid(row=0, column=1, pady=8, padx=10)

        ttk.Label(frame_compra, text="Selecione o Evento:").grid(row=1, column=0, sticky="w", pady=8)
        self.combo_evento = ttk.Combobox(frame_compra, state="readonly", width=42)
        self.combo_evento.grid(row=1, column=1, pady=8, padx=10)

        ttk.Label(frame_compra, text="Tipo de Ingresso (Base R$ 100,00):").grid(row=2, column=0, sticky="w", pady=8)
        self.combo_tipo = ttk.Combobox(
            frame_compra,
            state="readonly",
            width=42,
            values=["Inteira (R$ 100,00)", "Meia-Entrada (R$ 50,00)", "VIP (R$ 130,00)"]
        )
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=2, column=1, pady=8, padx=10)

        ttk.Button(frame_compra, text="Finalizar Compra", command=self._realizar_compra).grid(row=3, column=1, sticky="e", pady=15)

    def _atualizar_listas(self):
        # Atualiza Listbox de Eventos
        self.lista_eventos.delete(0, tk.END)
        nomes_eventos = []
        for ev in self.gerenciador.eventos:
            vagas = ev.capacidade_maxima - ev.ingressos_vendidos
            sessao_info = ev.sessoes[0].data_hora if ev.sessoes else "Sem sessão"
            self.lista_eventos.insert(
                tk.END,
                f"{ev.nome} [{ev.categoria.nome}] | Vagas: {vagas}/{ev.capacidade_maxima} | {sessao_info}"
            )
            nomes_eventos.append(ev.nome)

        self.combo_evento["values"] = nomes_eventos
        if nomes_eventos:
            self.combo_evento.current(0)

        # Atualiza Combobox de Participantes
        nomes_part = [f"{p.nome} ({p.identificacao})" for p in self.gerenciador.participantes]
        self.combo_participante["values"] = nomes_part
        if nomes_part:
            self.combo_participante.current(0)

    def _cadastrar_participante(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        cpf = self.entry_cpf.get().strip()

        if not nome or not email or not cpf:
            messagebox.showwarning("Campos Obrigatórios", "Preencha nome, e-mail e CPF.")
            return

        participante = Participante(nome, email, cpf)
        self.gerenciador.cadastrar_participante(participante)

        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)

        self._atualizar_listas()
        messagebox.showinfo("Sucesso", f"Participante '{nome}' cadastrado com sucesso!")

    def _realizar_compra(self):
        idx_p = self.combo_participante.current()
        idx_e = self.combo_evento.current()
        tipo_sel = self.combo_tipo.current()

        if idx_p < 0:
            messagebox.showerror("Erro", "Cadastre e selecione um participante antes de comprar.")
            return
        if idx_e < 0:
            messagebox.showerror("Erro", "Nenhum evento selecionado.")
            return

        participante = self.gerenciador.participantes[idx_p]
        evento = self.gerenciador.eventos[idx_e]

        preco_base = 100.0
        if tipo_sel == 0:
            ingresso = IngressoInteira(preco_base)
        elif tipo_sel == 1:
            ingresso = IngressoMeia(preco_base)
        else:
            ingresso = IngressoVIP(preco_base)

        try:
            # Chama a mesma regra de negócio do domínio
            inscricao = self.gerenciador.realizar_inscricao(participante, evento, ingresso, "Cartão")
            self._atualizar_listas()
            messagebox.showinfo("Compra Confirmada", inscricao.comprovante.obter_resumo())
        except Exception as erro:
            # Retorno visual do erro lançado pelo domínio (ex: lotação esgotada)
            messagebox.showerror("Não foi possível concluir", str(erro))
