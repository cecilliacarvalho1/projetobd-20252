import tkinter as tk
from tkinter import ttk, messagebox
from dao.escola_dao import EscolaDAO
from dao.turma_dao import TurmaDAO
from dao.professor_dao import ProfessorDAO
from dao.disciplina_dao import DisciplinaDAO
from dao.aula_dao import AulaDAO
from database.connection import db


class EscolaViewHierarquica:
    
    def __init__(self, parent):
        self.dao_escola = EscolaDAO()
        self.dao_turma = TurmaDAO()
        self.dao_professor = ProfessorDAO()
        self.dao_disciplina = DisciplinaDAO()
        self.dao_aula = AulaDAO()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciamento Escolar Hierárquico")
        self.window.geometry("1400x750")
        self.window.configure(bg='#ecf0f1')
        
        self.window.transient(parent)
        self.window.grab_set()
        
        self.selected_escola_id = None
        self.selected_turma_id = None
        self.selected_aula = None  # Armazena (id_turma, id_disciplina, id_professor)
        
        self.setup_style()
        self.create_widgets()
        self.load_escolas()
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       rowheight=28,
                       fieldbackground="#ffffff",
                       font=('Segoe UI', 9))
        
        style.map('Treeview', background=[('selected', '#3498db')])
        
        style.configure("Treeview.Heading",
                       background="#34495e",
                       foreground="white",
                       font=('Segoe UI', 10, 'bold'))
    
    def create_widgets(self):
        main_container = tk.Frame(self.window, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Cabeçalho
        header = tk.Frame(main_container, bg='#e67e22', relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X, pady=(0, 15))
        
        title = tk.Label(header,
                        text="🏫 Gestão Escolar: Escolas → Turmas → Professores/Disciplinas",
                        font=('Segoe UI', 16, 'bold'),
                        bg='#e67e22',
                        fg='white',
                        pady=12)
        title.pack()
        
        # Área principal (3 painéis)
        content_frame = tk.Frame(main_container, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_escolas_panel(content_frame)
        self.create_turmas_panel(content_frame)
        self.create_professores_panel(content_frame)
    
    def create_escolas_panel(self, parent):
        """Painel de Escolas"""
        escolas_frame = tk.Frame(parent, bg='#ffffff', relief=tk.RAISED, bd=2)
        escolas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        title = tk.Label(escolas_frame,
                        text="🏫 ESCOLAS",
                        font=('Segoe UI', 11, 'bold'),
                        bg='#34495e',
                        fg='white',
                        pady=8)
        title.pack(fill=tk.X)
        
        btn_frame = tk.Frame(escolas_frame, bg='#ffffff')
        btn_frame.pack(fill=tk.X, padx=8, pady=8)
        
        btns = [
            ("➕ Nova", self.adicionar_escola, '#27ae60'),
            ("✏️ Editar", self.editar_escola, '#f39c12'),
            ("🗑️ Excluir", self.excluir_escola, '#e74c3c')
        ]
        
        for text, cmd, color in btns:
            tk.Button(btn_frame, text=text, command=cmd,
                     font=('Segoe UI', 8, 'bold'), bg=color, fg='white',
                     relief=tk.FLAT, cursor='hand2', padx=8, pady=4
                     ).pack(side=tk.LEFT, padx=2)
        
        tree_container = tk.Frame(escolas_frame, bg='#ffffff')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_escolas = ttk.Treeview(tree_container,
                                         columns=("ID", "Nome", "Turmas"),
                                         show="headings",
                                         yscrollcommand=scrollbar.set,
                                         height=22)
        
        scrollbar.config(command=self.tree_escolas.yview)
        
        self.tree_escolas.heading("ID", text="ID")
        self.tree_escolas.heading("Nome", text="Nome da Escola")
        self.tree_escolas.heading("Turmas", text="Qtd Turmas")
        
        self.tree_escolas.column("ID", width=40, anchor=tk.CENTER)
        self.tree_escolas.column("Nome", width=280)
        self.tree_escolas.column("Turmas", width=80, anchor=tk.CENTER)
        
        self.tree_escolas.pack(fill=tk.BOTH, expand=True)
        self.tree_escolas.bind('<<TreeviewSelect>>', self.on_escola_select)
        
        self.count_escolas = tk.Label(escolas_frame, text="Total: 0 escolas",
                                      font=('Segoe UI', 8), bg='#ecf0f1',
                                      fg='#7f8c8d', pady=4)
        self.count_escolas.pack(fill=tk.X)
    
    def create_turmas_panel(self, parent):
        """Painel de Turmas"""
        turmas_frame = tk.Frame(parent, bg='#ffffff', relief=tk.RAISED, bd=2)
        turmas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        title = tk.Label(turmas_frame,
                        text="📚 TURMAS",
                        font=('Segoe UI', 11, 'bold'),
                        bg='#1abc9c',
                        fg='white',
                        pady=8)
        title.pack(fill=tk.X)
        
        self.escola_info = tk.Label(turmas_frame,
                                    text="← Selecione uma escola",
                                    font=('Segoe UI', 8, 'italic'),
                                    bg='#ecf0f1', fg='#7f8c8d', pady=4)
        self.escola_info.pack(fill=tk.X)
        
        btn_frame = tk.Frame(turmas_frame, bg='#ffffff')
        btn_frame.pack(fill=tk.X, padx=8, pady=8)
        
        btns = [
            ("➕ Nova", self.adicionar_turma, '#27ae60'),
            ("✏️ Editar", self.editar_turma, '#f39c12'),
            ("🗑️ Excluir", self.excluir_turma, '#e74c3c')
        ]
        
        for text, cmd, color in btns:
            tk.Button(btn_frame, text=text, command=cmd,
                     font=('Segoe UI', 8, 'bold'), bg=color, fg='white',
                     relief=tk.FLAT, cursor='hand2', padx=8, pady=4
                     ).pack(side=tk.LEFT, padx=2)
        
        tree_container = tk.Frame(turmas_frame, bg='#ffffff')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_turmas = ttk.Treeview(tree_container,
                                        columns=("ID", "Série", "Turma", "Turno", "Alunos"),
                                        show="headings",
                                        yscrollcommand=scrollbar.set,
                                        height=22)
        
        scrollbar.config(command=self.tree_turmas.yview)
        
        self.tree_turmas.heading("ID", text="ID")
        self.tree_turmas.heading("Série", text="Série")
        self.tree_turmas.heading("Turma", text="Turma")
        self.tree_turmas.heading("Turno", text="Turno")
        self.tree_turmas.heading("Alunos", text="Alunos")
        
        self.tree_turmas.column("ID", width=40, anchor=tk.CENTER)
        self.tree_turmas.column("Série", width=120)
        self.tree_turmas.column("Turma", width=60, anchor=tk.CENTER)
        self.tree_turmas.column("Turno", width=90, anchor=tk.CENTER)
        self.tree_turmas.column("Alunos", width=60, anchor=tk.CENTER)
        
        self.tree_turmas.pack(fill=tk.BOTH, expand=True)
        self.tree_turmas.bind('<<TreeviewSelect>>', self.on_turma_select)
        
        self.count_turmas = tk.Label(turmas_frame, text="Total: 0 turmas",
                                     font=('Segoe UI', 8), bg='#ecf0f1',
                                     fg='#7f8c8d', pady=4)
        self.count_turmas.pack(fill=tk.X)
    
    def create_professores_panel(self, parent):
        """Painel de Professores e Disciplinas"""
        prof_frame = tk.Frame(parent, bg='#ffffff', relief=tk.RAISED, bd=2)
        prof_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        title = tk.Label(prof_frame,
                        text="👨‍🏫 PROFESSORES & DISCIPLINAS",
                        font=('Segoe UI', 11, 'bold'),
                        bg='#8e44ad',
                        fg='white',
                        pady=8)
        title.pack(fill=tk.X)
        
        self.turma_info = tk.Label(prof_frame,
                                   text="← Selecione uma turma",
                                   font=('Segoe UI', 8, 'italic'),
                                   bg='#ecf0f1', fg='#7f8c8d', pady=4)
        self.turma_info.pack(fill=tk.X)
        
        btn_frame = tk.Frame(prof_frame, bg='#ffffff')
        btn_frame.pack(fill=tk.X, padx=8, pady=8)
        
        btns = [
            ("➕ Atribuir", self.atribuir_professor, '#27ae60'),
            ("✏️ Alterar Prof", self.alterar_professor, '#f39c12'),
            ("🗑️ Remover", self.remover_atribuicao, '#e74c3c')
        ]
        
        for text, cmd, color in btns:
            tk.Button(btn_frame, text=text, command=cmd,
                     font=('Segoe UI', 8, 'bold'), bg=color, fg='white',
                     relief=tk.FLAT, cursor='hand2', padx=8, pady=4
                     ).pack(side=tk.LEFT, padx=2)
        
        tree_container = tk.Frame(prof_frame, bg='#ffffff')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_professores = ttk.Treeview(tree_container,
                                             columns=("Disciplina", "Professor", "Carga"),
                                             show="headings",
                                             yscrollcommand=scrollbar.set,
                                             height=22)
        
        scrollbar.config(command=self.tree_professores.yview)
        
        self.tree_professores.heading("Disciplina", text="Disciplina")
        self.tree_professores.heading("Professor", text="Professor")
        self.tree_professores.heading("Carga", text="Carga H.")
        
        self.tree_professores.column("Disciplina", width=140)
        self.tree_professores.column("Professor", width=200)
        self.tree_professores.column("Carga", width=70, anchor=tk.CENTER)
        
        self.tree_professores.pack(fill=tk.BOTH, expand=True)
        self.tree_professores.bind('<<TreeviewSelect>>', self.on_professor_select)
        
        self.count_professores = tk.Label(prof_frame, text="Total: 0 atribuições",
                                         font=('Segoe UI', 8), bg='#ecf0f1',
                                         fg='#7f8c8d', pady=4)
        self.count_professores.pack(fill=tk.X)
    
    # ===== CARREGAMENTO DE DADOS =====
    
    def load_escolas(self):
        for item in self.tree_escolas.get_children():
            self.tree_escolas.delete(item)
        
        try:
            escolas = self.dao_escola.listar_com_turmas()
            for escola in escolas:
                self.tree_escolas.insert('', tk.END, values=(
                    escola['id_escola'],
                    escola['nome'],
                    escola['total_turmas']
                ))
            self.count_escolas.config(text=f"Total: {len(escolas)} escolas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar escolas: {e}")
    
    def load_turmas(self, id_escola):
        for item in self.tree_turmas.get_children():
            self.tree_turmas.delete(item)
        
        try:
            query = """
                SELECT 
                    t.id_turma,
                    s.nome as serie_nome,
                    t.nome as turma_nome,
                    t.turno,
                    COUNT(m.id_matricula) as total_alunos
                FROM Turma t
                INNER JOIN Serie s ON t.id_serie = s.id_serie
                LEFT JOIN Matricula m ON t.id_turma = m.id_turma AND m.status = 'Ativo'
                WHERE t.id_escola = %s
                GROUP BY t.id_turma
                ORDER BY s.nome, t.nome
            """
            
            turmas = db.execute_query(query, (id_escola,), fetch=True)
            
            for turma in turmas:
                self.tree_turmas.insert('', tk.END, values=(
                    turma['id_turma'],
                    turma['serie_nome'],
                    turma['turma_nome'],
                    turma['turno'],
                    turma['total_alunos']
                ))
            
            self.count_turmas.config(text=f"Total: {len(turmas)} turmas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar turmas: {e}")
    
    def load_professores_disciplinas(self, id_turma):
        for item in self.tree_professores.get_children():
            self.tree_professores.delete(item)
        
        try:
            atribuicoes = self.dao_aula.listar_por_turma(id_turma)
            
            for atr in atribuicoes:
                # --- CORREÇÃO DE HORAS ---
                raw_carga = atr['carga_horaria']
                carga_exibida = str(raw_carga)
                
                # Se for objeto de tempo (timedelta)
                if hasattr(raw_carga, 'total_seconds'):
                    horas_totais = int(raw_carga.total_seconds() // 3600)
                    carga_exibida = f"{horas_totais}h"
                
                # Se vier como string "200:00:00"
                elif isinstance(raw_carga, str) and ':' in raw_carga:
                    try:
                        horas_totais = int(raw_carga.split(':')[0])
                        carga_exibida = f"{horas_totais}h"
                    except:
                        pass
                
                item_id = self.tree_professores.insert('', tk.END, values=(
                    atr['disciplina_nome'],
                    atr['professor_nome'],
                    carga_exibida
                ))
                
                self.tree_professores.item(item_id, tags=(
                    atr['id_turma'],
                    atr['id_disciplina'],
                    atr['id_professor']
                ))
            
            self.count_professores.config(text=f"Total: {len(atribuicoes)} atribuições")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar atribuições: {e}")
    
    # ===== EVENTOS DE SELEÇÃO =====
    
    def on_escola_select(self, event):
        selection = self.tree_escolas.selection()
        if selection:
            item = self.tree_escolas.item(selection[0])
            self.selected_escola_id = item['values'][0]
            escola_nome = item['values'][1]
            
            self.escola_info.config(text=f"📌 Escola: {escola_nome}")
            self.load_turmas(self.selected_escola_id)
            
            # Limpar painel de professores
            for item in self.tree_professores.get_children():
                self.tree_professores.delete(item)
            self.turma_info.config(text="← Selecione uma turma")
            self.count_professores.config(text="Total: 0 atribuições")
    
    def on_turma_select(self, event):
        selection = self.tree_turmas.selection()
        if selection:
            item = self.tree_turmas.item(selection[0])
            self.selected_turma_id = item['values'][0]
            serie = item['values'][1]
            turma = item['values'][2]
            turno = item['values'][3]
            
            self.turma_info.config(text=f"📌 Turma: {serie} - {turma} ({turno})")
            self.load_professores_disciplinas(self.selected_turma_id)
    
    def on_professor_select(self, event):
        selection = self.tree_professores.selection()
        if selection:
            item = self.tree_professores.item(selection[0])
            tags = item['tags']
            if len(tags) >= 3:
                self.selected_aula = {
                    'id_turma': int(tags[0]),
                    'id_disciplina': int(tags[1]),
                    'id_professor': int(tags[2])
                }
    
    # ===== OPERAÇÕES COM ESCOLAS =====
    
    def adicionar_escola(self):
        try:
            from views.escola_form import EscolaForm
            EscolaForm(self.window, self.dao_escola, callback=self.load_escolas)
        except ImportError:
            messagebox.showerror("Erro", "Formulário 'views/escola_form.py' não encontrado.")
    
    def editar_escola(self):
        if not self.selected_escola_id:
            messagebox.showwarning("Atenção", "Selecione uma escola!")
            return
        
        try:
            from views.escola_form import EscolaForm
            escola = self.dao_escola.read(self.selected_escola_id)
            EscolaForm(self.window, self.dao_escola, escola=escola, callback=self.load_escolas)
        except ImportError:
            messagebox.showerror("Erro", "Formulário 'views/escola_form.py' não encontrado.")
    
    def excluir_escola(self):
        if not self.selected_escola_id:
            messagebox.showwarning("Atenção", "Selecione uma escola!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta escola?"):
            try:
                self.dao_escola.delete(self.selected_escola_id)
                messagebox.showinfo("Sucesso", "Escola excluída com sucesso!")
                self.selected_escola_id = None
                self.load_escolas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")
    
    # ===== OPERAÇÕES COM TURMAS (ATUALIZADO) =====
    
    def adicionar_turma(self):
        if not self.selected_escola_id:
            messagebox.showwarning("Atenção", "Selecione uma escola primeiro!")
            return
        
        try:
            from views.turma_form import TurmaForm
            TurmaForm(self.window, self.dao_turma, id_escola=self.selected_escola_id,
                     callback=lambda: self.load_turmas(self.selected_escola_id))
        except ImportError as e:
            messagebox.showerror("Erro de Arquivo", f"Não foi possível encontrar 'turma_form.py' na pasta views.\nErro: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir formulário: {e}")
    
    def editar_turma(self):
        if not self.selected_turma_id:
            messagebox.showwarning("Atenção", "Selecione uma turma!")
            return
        
        try:
            from views.turma_form import TurmaForm
            turma = self.dao_turma.read(self.selected_turma_id)
            TurmaForm(self.window, self.dao_turma, turma=turma,
                     callback=lambda: self.load_turmas(self.selected_escola_id))
        except ImportError as e:
            messagebox.showerror("Erro de Arquivo", f"Não foi possível encontrar 'turma_form.py' na pasta views.\nErro: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir formulário: {e}")
    
    def excluir_turma(self):
        if not self.selected_turma_id:
            messagebox.showwarning("Atenção", "Selecione uma turma!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta turma?"):
            try:
                self.dao_turma.delete(self.selected_turma_id)
                messagebox.showinfo("Sucesso", "Turma excluída com sucesso!")
                self.selected_turma_id = None
                self.load_turmas(self.selected_escola_id)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")
    
    # ===== OPERAÇÕES COM PROFESSORES/DISCIPLINAS (ATUALIZADO) =====
    
    def atribuir_professor(self):
        if not self.selected_turma_id:
            messagebox.showwarning("Atenção", "Selecione uma turma primeiro!")
            return
        
        try:
            from views.atribuicao_form import AtribuicaoForm
            AtribuicaoForm(self.window, self.dao_aula, self.dao_disciplina, 
                          self.dao_professor, id_turma=self.selected_turma_id,
                          callback=lambda: self.load_professores_disciplinas(self.selected_turma_id))
        except ImportError as e:
            messagebox.showerror("Erro de Arquivo", f"Não foi possível encontrar 'atribuicao_form.py' na pasta views.\nErro: {e}")
    
    def alterar_professor(self):
        if not self.selected_aula:
            messagebox.showwarning("Atenção", "Selecione uma atribuição!")
            return
        
        try:
            from views.alterar_professor_form import AlterarProfessorForm
            AlterarProfessorForm(self.window, self.dao_aula, self.dao_professor,
                                atribuicao=self.selected_aula,
                                callback=lambda: self.load_professores_disciplinas(self.selected_turma_id))
        except ImportError as e:
            messagebox.showerror("Erro de Arquivo", f"Não foi possível encontrar 'alterar_professor_form.py' na pasta views.\nErro: {e}")
    
    def remover_atribuicao(self):
        if not self.selected_aula:
            messagebox.showwarning("Atenção", "Selecione uma atribuição!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente remover esta atribuição?"):
            try:
                self.dao_aula.remover_atribuicao(
                    self.selected_aula['id_turma'],
                    self.selected_aula['id_disciplina'],
                    self.selected_aula['id_professor']
                )
                messagebox.showinfo("Sucesso", "Atribuição removida com sucesso!")
                self.selected_aula = None
                self.load_professores_disciplinas(self.selected_turma_id)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover: {e}")