import tkinter as tk
from tkinter import ttk, messagebox
from dao.turma_dao import TurmaDAO
from dao.escola_dao import EscolaDAO
from database.connection import db


class TurmaView:
    
    def __init__(self, parent):
        self.dao = TurmaDAO()
        self.dao_escola = EscolaDAO()
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Turmas")
        self.window.geometry("1100x700")
        self.window.configure(bg='#ecf0f1')
        
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.selected_id = None
        
        self.setup_style()
        self.create_widgets()
        self.load_data()
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       rowheight=30,
                       fieldbackground="#ffffff",
                       font=('Segoe UI', 10))
        
        style.map('Treeview',
                 background=[('selected', '#1abc9c')])
        
        style.configure("Treeview.Heading",
                       background="#34495e",
                       foreground="white",
                       font=('Segoe UI', 11, 'bold'))
    
    def create_widgets(self):
        main_container = tk.Frame(self.window, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header = tk.Frame(main_container, bg='#1abc9c', relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(header,
                        text="📚 Gerenciamento de Turmas",
                        font=('Segoe UI', 18, 'bold'),
                        bg='#1abc9c',
                        fg='white',
                        pady=15)
        title.pack()
        
        content_frame = tk.Frame(main_container, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # COLUNA ESQUERDA - Formulário
        left_panel = tk.Frame(content_frame, bg='#ecf0f1')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        form_frame = tk.Frame(left_panel, bg='#ffffff', relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        form_title = tk.Label(form_frame,
                             text="📝 Dados da Turma",
                             font=('Segoe UI', 13, 'bold'),
                             bg='#34495e',
                             fg='white',
                             pady=10)
        form_title.pack(fill=tk.X)
        
        fields_container = tk.Frame(form_frame, bg='#ffffff')
        fields_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Escola
        tk.Label(fields_container,
                text="Escola:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=0, column=0, sticky=tk.W, pady=10)
        
        escolas = self.dao_escola.read_all()
        self.escolas_dict = {f"{e['id_escola']} - {e['nome']}": e['id_escola'] for e in escolas}
        
        self.escola_var = tk.StringVar()
        escola_combo = ttk.Combobox(fields_container,
                                   textvariable=self.escola_var,
                                   values=list(self.escolas_dict.keys()),
                                   state="readonly",
                                   font=('Segoe UI', 9),
                                   width=33)
        escola_combo.grid(row=0, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        escola_combo.bind('<<ComboboxSelected>>', self.on_escola_select)
        
        # Série
        tk.Label(fields_container,
                text="Série:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=1, column=0, sticky=tk.W, pady=10)
        
        # Buscar séries
        query = "SELECT id_serie, nome, nivel FROM Serie ORDER BY id_serie"
        series = db.execute_query(query, fetch=True)
        self.series_dict = {f"{s['nome']} - {s['nivel']}": s['id_serie'] for s in series}
        
        self.serie_var = tk.StringVar()
        serie_combo = ttk.Combobox(fields_container,
                                  textvariable=self.serie_var,
                                  values=list(self.series_dict.keys()),
                                  state="readonly",
                                  font=('Segoe UI', 9),
                                  width=33)
        serie_combo.grid(row=1, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Nome da Turma
        tk.Label(fields_container,
                text="Nome (A, B, C...):",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=2, column=0, sticky=tk.W, pady=10)
        
        self.nome_var = tk.StringVar(value="A")
        nome_combo = ttk.Combobox(fields_container,
                                 textvariable=self.nome_var,
                                 values=["A", "B", "C", "D", "E"],
                                 state="readonly",
                                 font=('Segoe UI', 9),
                                 width=33)
        nome_combo.grid(row=2, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Turno
        tk.Label(fields_container,
                text="Turno:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=3, column=0, sticky=tk.W, pady=10)
        
        self.turno_var = tk.StringVar(value="Matutino")
        turno_combo = ttk.Combobox(fields_container,
                                   textvariable=self.turno_var,
                                   values=["Matutino", "Vespertino"],
                                   state="readonly",
                                   font=('Segoe UI', 9),
                                   width=33)
        turno_combo.grid(row=3, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Ano Letivo
        tk.Label(fields_container,
                text="Ano Letivo:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=4, column=0, sticky=tk.W, pady=10)
        
        self.ano_entry = tk.Entry(fields_container,
                                  font=('Segoe UI', 10),
                                  relief=tk.FLAT,
                                  bg='#ecf0f1',
                                  width=35,
                                  bd=2)
        self.ano_entry.insert(0, "2024")
        self.ano_entry.grid(row=4, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Capacidade
        tk.Label(fields_container,
                text="Capacidade:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=5, column=0, sticky=tk.W, pady=10)
        
        self.capacidade_entry = tk.Entry(fields_container,
                                        font=('Segoe UI', 10),
                                        relief=tk.FLAT,
                                        bg='#ecf0f1',
                                        width=35,
                                        bd=2)
        self.capacidade_entry.insert(0, "30")
        self.capacidade_entry.grid(row=5, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Botões
        buttons_frame = tk.Frame(form_frame, bg='#ffffff')
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        btn_configs = [
            ("💾 Salvar", self.salvar, '#27ae60', '#229954'),
            ("✏️ Editar", self.editar, '#f39c12', '#d68910'),
            ("🗑️ Deletar", self.deletar, '#e74c3c', '#c0392b'),
            ("🔄 Limpar", self.limpar, '#95a5a6', '#7f8c8d'),
        ]
        
        for i, (text, command, bg, active_bg) in enumerate(btn_configs):
            btn = tk.Button(buttons_frame,
                          text=text,
                          command=command,
                          font=('Segoe UI', 10, 'bold'),
                          bg=bg,
                          fg='white',
                          activebackground=active_bg,
                          activeforeground='white',
                          relief=tk.FLAT,
                          cursor='hand2',
                          padx=15,
                          pady=8)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
        
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # COLUNA DIREITA - Tabela
        right_panel = tk.Frame(content_frame, bg='#ecf0f1')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Filtro
        filter_frame = tk.Frame(right_panel, bg='#ffffff', relief=tk.RAISED, bd=2)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        filter_title = tk.Label(filter_frame,
                               text="🔍 Filtrar Turmas",
                               font=('Segoe UI', 11, 'bold'),
                               bg='#34495e',
                               fg='white',
                               pady=8)
        filter_title.pack(fill=tk.X)
        
        filter_container = tk.Frame(filter_frame, bg='#ffffff')
        filter_container.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Button(filter_container,
                 text="Listar Todos",
                 command=self.load_data,
                 font=('Segoe UI', 9, 'bold'),
                 bg='#1abc9c',
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 padx=20,
                 pady=5).pack(side=tk.LEFT, padx=5)
        
        # Tabela
        table_frame = tk.Frame(right_panel, bg='#ffffff', relief=tk.RAISED, bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        table_title = tk.Label(table_frame,
                              text="📋 Lista de Turmas",
                              font=('Segoe UI', 11, 'bold'),
                              bg='#34495e',
                              fg='white',
                              pady=8)
        table_title.pack(fill=tk.X)
        
        tree_container = tk.Frame(table_frame, bg='#ffffff')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_y = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ("ID", "Escola", "Série", "Turma", "Turno", "Ano", "Vagas", "Alunos")
        self.tree = ttk.Treeview(tree_container,
                                columns=columns,
                                show="headings",
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set,
                                height=15)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Escola", width=180)
        self.tree.column("Série", width=100)
        self.tree.column("Turma", width=60, anchor=tk.CENTER)
        self.tree.column("Turno", width=90, anchor=tk.CENTER)
        self.tree.column("Ano", width=60, anchor=tk.CENTER)
        self.tree.column("Vagas", width=60, anchor=tk.CENTER)
        self.tree.column("Alunos", width=70, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.count_label = tk.Label(table_frame,
                                    text="Total: 0 turmas",
                                    font=('Segoe UI', 9),
                                    bg='#ecf0f1',
                                    fg='#7f8c8d',
                                    pady=5)
        self.count_label.pack(fill=tk.X)
    
    def on_escola_select(self, event):
        """Callback quando seleciona escola"""
        pass
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            turmas = self.dao.listar_completo()
            for turma in turmas:
                vagas_disponiveis = turma['capacidade'] - turma['total_alunos']
                self.tree.insert('', tk.END, values=(
                    turma['id_turma'],
                    turma['escola_nome'],
                    turma['serie_nome'],
                    turma['turma_nome'],
                    turma['turno'],
                    turma['ano_letivo'],
                    vagas_disponiveis,
                    turma['total_alunos']
                ))
            
            self.count_label.config(text=f"Total: {len(turmas)} turmas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def salvar(self):
        if not self.escola_var.get():
            messagebox.showwarning("Atenção", "Selecione uma escola!")
            return
        
        if not self.serie_var.get():
            messagebox.showwarning("Atenção", "Selecione uma série!")
            return
        
        data = {
            'id_escola': self.escolas_dict[self.escola_var.get()],
            'id_serie': self.series_dict[self.serie_var.get()],
            'nome': self.nome_var.get(),
            'turno': self.turno_var.get(),
            'ano_letivo': int(self.ano_entry.get()),
            'capacidade': int(self.capacidade_entry.get())
        }
        
        try:
            if self.selected_id is None:
                self.dao.create(data)
                messagebox.showinfo("✓ Sucesso", "Turma cadastrada com sucesso!")
            else:
                self.dao.update(self.selected_id, data)
                messagebox.showinfo("✓ Sucesso", "Turma atualizada com sucesso!")
            
            self.limpar()
            self.load_data()
        except Exception as e:
            messagebox.showerror("✗ Erro", f"Erro ao salvar: {e}")
    
    def editar(self):
        if self.selected_id is None:
            messagebox.showwarning("Atenção", "Selecione uma turma na tabela!")
            return
        
        try:
            turma = self.dao.read(self.selected_id)
            if turma:
                # Encontrar escola
                for key, value in self.escolas_dict.items():
                    if value == turma['id_escola']:
                        self.escola_var.set(key)
                        break
                
                # Encontrar série
                for key, value in self.series_dict.items():
                    if value == turma['id_serie']:
                        self.serie_var.set(key)
                        break
                
                self.nome_var.set(turma['nome'])
                self.turno_var.set(turma['turno'])
                
                self.ano_entry.delete(0, tk.END)
                self.ano_entry.insert(0, turma['ano_letivo'])
                
                self.capacidade_entry.delete(0, tk.END)
                self.capacidade_entry.insert(0, turma['capacidade'])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar turma: {e}")
    
    def deletar(self):
        if self.selected_id is None:
            messagebox.showwarning("Atenção", "Selecione uma turma na tabela!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente deletar esta turma?"):
            try:
                self.dao.delete(self.selected_id)
                messagebox.showinfo("✓ Sucesso", "Turma deletada com sucesso!")
                self.limpar()
                self.load_data()
            except Exception as e:
                messagebox.showerror("✗ Erro", f"Erro ao deletar: {e}")
    
    def limpar(self):
        self.escola_var.set('')
        self.serie_var.set('')
        self.nome_var.set('A')
        self.turno_var.set('Matutino')
        self.ano_entry.delete(0, tk.END)
        self.ano_entry.insert(0, '2024')
        self.capacidade_entry.delete(0, tk.END)
        self.capacidade_entry.insert(0, '30')
        self.selected_id = None
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_id = item['values'][0]