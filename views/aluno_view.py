import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from dao.aluno_dao import AlunoDAO


class AlunoView:
    
    def __init__(self, parent):
        self.dao = AlunoDAO()
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Alunos")
        self.window.geometry("1100x700")
        self.window.configure(bg='#ecf0f1')
        
        # Tornar a janela modal (impede interação com a janela principal)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Impedir redimensionamento
        self.window.resizable(False, False)
        
        self.selected_id = None
        
        self.setup_style()
        self.create_widgets()
        self.load_data()
    
    def setup_style(self):
        """Configura estilos modernos"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar Treeview
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       rowheight=30,
                       fieldbackground="#ffffff",
                       font=('Segoe UI', 10))
        
        style.map('Treeview',
                 background=[('selected', '#3498db')])
        
        style.configure("Treeview.Heading",
                       background="#34495e",
                       foreground="white",
                       font=('Segoe UI', 11, 'bold'))
        
        # Labels
        style.configure('Form.TLabel',
                       font=('Segoe UI', 10),
                       background='#ffffff')
        
        # Entries
        style.configure('Form.TEntry',
                       fieldbackground='#ecf0f1',
                       font=('Segoe UI', 10))
    
    def create_widgets(self):
        # Container principal
        main_container = tk.Frame(self.window, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === CABEÇALHO ===
        header = tk.Frame(main_container, bg='#3498db', relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(header,
                        text="👨‍🎓 Gerenciamento de Alunos",
                        font=('Segoe UI', 18, 'bold'),
                        bg='#3498db',
                        fg='white',
                        pady=15)
        title.pack()
        
        # === ÁREA PRINCIPAL (2 colunas) ===
        content_frame = tk.Frame(main_container, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # COLUNA ESQUERDA - Formulário
        left_panel = tk.Frame(content_frame, bg='#ecf0f1')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Formulário
        form_frame = tk.Frame(left_panel, bg='#ffffff', relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        form_title = tk.Label(form_frame,
                             text="📝 Dados do Aluno",
                             font=('Segoe UI', 13, 'bold'),
                             bg='#34495e',
                             fg='white',
                             pady=10)
        form_title.pack(fill=tk.X)
        
        # Container dos campos
        fields_container = tk.Frame(form_frame, bg='#ffffff')
        fields_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.entries = {}
        fields = [
            ("Nome Completo:", "nome"),
            ("CPF:", "cpf"),
            ("Telefone:", "telefone"),
            ("Email:", "email"),
            ("Endereço:", "endereco"),
            ("Data Nasc. (AAAA-MM-DD):", "data_nascimento"),
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            tk.Label(fields_container,
                    text=label_text,
                    font=('Segoe UI', 10, 'bold'),
                    bg='#ffffff',
                    fg='#2c3e50',
                    anchor='w').grid(row=i, column=0, sticky=tk.W, pady=8)
            
            entry = tk.Entry(fields_container,
                           font=('Segoe UI', 10),
                           relief=tk.FLAT,
                           bg='#ecf0f1',
                           width=30,
                           bd=2)
            entry.grid(row=i, column=1, sticky=tk.W, pady=8, padx=(10, 0))
            self.entries[field_name] = entry
        
        # Sexo
        tk.Label(fields_container,
                text="Sexo:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=len(fields), column=0, sticky=tk.W, pady=8)
        
        self.sexo_var = tk.StringVar(value="Masculino")
        sexo_frame = tk.Frame(fields_container, bg='#ffffff')
        sexo_frame.grid(row=len(fields), column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        tk.Radiobutton(sexo_frame, text="Masculino", variable=self.sexo_var,
                      value="Masculino", bg='#ffffff', font=('Segoe UI', 9),
                      selectcolor='#3498db').pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(sexo_frame, text="Feminino", variable=self.sexo_var,
                      value="Feminino", bg='#ffffff', font=('Segoe UI', 9),
                      selectcolor='#3498db').pack(side=tk.LEFT)
        
        # Status
        tk.Label(fields_container,
                text="Status:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w').grid(row=len(fields)+1, column=0, sticky=tk.W, pady=8)
        
        self.status_var = tk.StringVar(value="Ativo")
        status_combo = ttk.Combobox(fields_container,
                                   textvariable=self.status_var,
                                   values=["Ativo", "Inativo"],
                                   state="readonly",
                                   font=('Segoe UI', 10),
                                   width=28)
        status_combo.grid(row=len(fields)+1, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        # Botões de ação
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
        
        # Área de busca
        search_frame = tk.Frame(right_panel, bg='#ffffff', relief=tk.RAISED, bd=2)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_title = tk.Label(search_frame,
                               text="🔍 Buscar Aluno",
                               font=('Segoe UI', 11, 'bold'),
                               bg='#34495e',
                               fg='white',
                               pady=8)
        search_title.pack(fill=tk.X)
        
        search_container = tk.Frame(search_frame, bg='#ffffff')
        search_container.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(search_container,
                text="Nome:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff').pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = tk.Entry(search_container,
                                     font=('Segoe UI', 10),
                                     relief=tk.FLAT,
                                     bg='#ecf0f1',
                                     width=25,
                                     bd=2)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(search_container,
                 text="Buscar",
                 command=self.buscar,
                 font=('Segoe UI', 9, 'bold'),
                 bg='#3498db',
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 padx=15,
                 pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_container,
                 text="Listar Todos",
                 command=self.load_data,
                 font=('Segoe UI', 9, 'bold'),
                 bg='#16a085',
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 padx=15,
                 pady=5).pack(side=tk.LEFT, padx=5)
        
        # Tabela
        table_frame = tk.Frame(right_panel, bg='#ffffff', relief=tk.RAISED, bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        table_title = tk.Label(table_frame,
                              text="📋 Lista de Alunos",
                              font=('Segoe UI', 11, 'bold'),
                              bg='#34495e',
                              fg='white',
                              pady=8)
        table_title.pack(fill=tk.X)
        
        # Scrollbar e Treeview
        tree_container = tk.Frame(table_frame, bg='#ffffff')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ("ID", "Nome", "CPF", "Sexo", "Telefone", "Email", "Endereço", "Data Nasc.", "Data Cadastro", "Status")
        self.tree = ttk.Treeview(tree_container,
                                columns=columns,
                                show="headings",
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set,
                                height=15)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Sexo", text="Sexo")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Data Nasc.", text="Data Nascimento")
        self.tree.heading("Data Cadastro", text="Data Cadastro")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nome", width=200)
        self.tree.column("CPF", width=110, anchor=tk.CENTER)
        self.tree.column("Sexo", width=80, anchor=tk.CENTER)
        self.tree.column("Telefone", width=110, anchor=tk.CENTER)
        self.tree.column("Email", width=200)
        self.tree.column("Endereço", width=250)
        self.tree.column("Data Nasc.", width=110, anchor=tk.CENTER)
        self.tree.column("Data Cadastro", width=110, anchor=tk.CENTER)
        self.tree.column("Status", width=70, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Contador de registros
        self.count_label = tk.Label(table_frame,
                                    text="Total: 0 alunos",
                                    font=('Segoe UI', 9),
                                    bg='#ecf0f1',
                                    fg='#7f8c8d',
                                    pady=5)
        self.count_label.pack(fill=tk.X)
    
    def load_data(self):
        """Carrega todos os alunos na tabela"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            alunos = self.dao.read_all()
            for aluno in alunos:
                self.tree.insert('', tk.END, values=(
                    aluno['id_aluno'],
                    aluno['nome'],
                    aluno['cpf'] or 'N/A',
                    aluno['sexo'] or 'N/A',
                    aluno['telefone'],
                    aluno['email'] or 'N/A',
                    aluno['endereco'] or 'N/A',
                    aluno['data_nascimento'] or 'N/A',
                    aluno['data_cadastro'] or 'N/A',
                    aluno['status']
                ))
            
            self.count_label.config(text=f"Total: {len(alunos)} alunos")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def salvar(self):
        """Salva um novo aluno ou atualiza existente"""
        if not self.entries['nome'].get():
            messagebox.showwarning("Atenção", "Nome é obrigatório!")
            return
        
        data = {
            'nome': self.entries['nome'].get(),
            'cpf': self.entries['cpf'].get() or None,
            'sexo': self.sexo_var.get(),
            'endereco': self.entries['endereco'].get() or None,
            'telefone': self.entries['telefone'].get(),
            'email': self.entries['email'].get() or None,
            'data_nascimento': self.entries['data_nascimento'].get() or date.today(),
            'data_cadastro': date.today(),
            'status': self.status_var.get()
        }
        
        try:
            if self.selected_id is None:
                self.dao.create(data)
                messagebox.showinfo("✓ Sucesso", "Aluno cadastrado com sucesso!")
            else:
                self.dao.update(self.selected_id, data)
                messagebox.showinfo("✓ Sucesso", "Aluno atualizado com sucesso!")
            
            self.limpar()
            self.load_data()
        except Exception as e:
            messagebox.showerror("✗ Erro", f"Erro ao salvar: {e}")
    
    def editar(self):
        """Prepara o formulário para editar"""
        if self.selected_id is None:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela!")
            return
        
        try:
            aluno = self.dao.read(self.selected_id)
            if aluno:
                self.entries['nome'].delete(0, tk.END)
                self.entries['nome'].insert(0, aluno['nome'])
                
                self.entries['cpf'].delete(0, tk.END)
                self.entries['cpf'].insert(0, aluno['cpf'] or '')
                
                self.entries['telefone'].delete(0, tk.END)
                self.entries['telefone'].insert(0, aluno['telefone'])
                
                self.entries['email'].delete(0, tk.END)
                self.entries['email'].insert(0, aluno['email'] or '')
                
                self.entries['endereco'].delete(0, tk.END)
                self.entries['endereco'].insert(0, aluno['endereco'] or '')
                
                self.entries['data_nascimento'].delete(0, tk.END)
                self.entries['data_nascimento'].insert(0, str(aluno['data_nascimento']))
                
                self.sexo_var.set(aluno['sexo'])
                self.status_var.set(aluno['status'])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar aluno: {e}")
    
    def deletar(self):
        """Deleta o aluno selecionado"""
        if self.selected_id is None:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente deletar este aluno?"):
            try:
                self.dao.delete(self.selected_id)
                messagebox.showinfo("✓ Sucesso", "Aluno deletado com sucesso!")
                self.limpar()
                self.load_data()
            except Exception as e:
                messagebox.showerror("✗ Erro", f"Erro ao deletar: {e}")
    
    def buscar(self):
        """Busca alunos por nome"""
        nome = self.search_entry.get()
        
        if not nome:
            messagebox.showwarning("Atenção", "Digite um nome para buscar!")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            alunos = self.dao.buscar_por_nome(nome)
            
            if not alunos:
                messagebox.showinfo("Resultado", "Nenhum aluno encontrado!")
                self.count_label.config(text="Total: 0 alunos")
                return
            
            for aluno in alunos:
                self.tree.insert('', tk.END, values=(
                    aluno['id_aluno'],
                    aluno['nome'],
                    aluno['cpf'] or 'N/A',
                    aluno['sexo'] or 'N/A',
                    aluno['telefone'],
                    aluno['email'] or 'N/A',
                    aluno['endereco'] or 'N/A',
                    aluno['data_nascimento'] or 'N/A',
                    aluno['data_cadastro'] or 'N/A',
                    aluno['status']
                ))
            
            self.count_label.config(text=f"Total: {len(alunos)} alunos encontrados")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {e}")
    
    def limpar(self):
        """Limpa todos os campos"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        self.sexo_var.set("Masculino")
        self.status_var.set("Ativo")
        self.selected_id = None
        self.search_entry.delete(0, tk.END)
    
    def on_select(self, event):
        """Callback quando seleciona item na tabela"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_id = item['values'][0]