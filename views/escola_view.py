import tkinter as tk
from tkinter import ttk, messagebox
from dao.escola_dao import EscolaDAO


class EscolaView:
    
    def __init__(self, parent):
        self.dao = EscolaDAO()
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Escolas")
        self.window.geometry("1100x700")
        self.window.configure(bg='#ecf0f1')
        
        # Modal
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.selected_id = None
        
        self.setup_style()
        self.create_widgets()
        self.load_data()
    
    def setup_style(self):
        """Configura estilos modernos"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       rowheight=30,
                       fieldbackground="#ffffff",
                       font=('Segoe UI', 10))
        
        style.map('Treeview',
                 background=[('selected', '#e67e22')])
        
        style.configure("Treeview.Heading",
                       background="#34495e",
                       foreground="white",
                       font=('Segoe UI', 11, 'bold'))
    
    def create_widgets(self):
        main_container = tk.Frame(self.window, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header = tk.Frame(main_container, bg='#e67e22', relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(header,
                        text="🏫 Gerenciamento de Escolas",
                        font=('Segoe UI', 18, 'bold'),
                        bg='#e67e22',
                        fg='white',
                        pady=15)
        title.pack()
        
        # Área principal (2 colunas)
        content_frame = tk.Frame(main_container, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # COLUNA ESQUERDA - Formulário
        left_panel = tk.Frame(content_frame, bg='#ecf0f1')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        form_frame = tk.Frame(left_panel, bg='#ffffff', relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        form_title = tk.Label(form_frame,
                             text="📝 Dados da Escola",
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
            ("Nome da Escola:", "nome"),
            ("Endereço:", "endereco"),
            ("Telefone:", "telefone"),
            ("Diretor(a):", "diretor"),
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            tk.Label(fields_container,
                    text=label_text,
                    font=('Segoe UI', 10, 'bold'),
                    bg='#ffffff',
                    fg='#2c3e50',
                    anchor='w').grid(row=i, column=0, sticky=tk.W, pady=12)
            
            entry = tk.Entry(fields_container,
                           font=('Segoe UI', 10),
                           relief=tk.FLAT,
                           bg='#ecf0f1',
                           width=35,
                           bd=2)
            entry.grid(row=i, column=1, sticky=tk.W, pady=12, padx=(10, 0))
            self.entries[field_name] = entry
        
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
                               text="🔍 Buscar Escola",
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
                 bg='#e67e22',
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
                              text="📋 Lista de Escolas",
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
        
        columns = ("ID", "Nome", "Endereço", "Telefone", "Diretor", "Total Turmas")
        self.tree = ttk.Treeview(tree_container,
                                columns=columns,
                                show="headings",
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set,
                                height=15)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Diretor", text="Diretor(a)")
        self.tree.heading("Total Turmas", text="Turmas")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nome", width=200)
        self.tree.column("Endereço", width=250)
        self.tree.column("Telefone", width=110, anchor=tk.CENTER)
        self.tree.column("Diretor", width=150)
        self.tree.column("Total Turmas", width=80, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.count_label = tk.Label(table_frame,
                                    text="Total: 0 escolas",
                                    font=('Segoe UI', 9),
                                    bg='#ecf0f1',
                                    fg='#7f8c8d',
                                    pady=5)
        self.count_label.pack(fill=tk.X)
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            escolas = self.dao.listar_com_turmas()
            for escola in escolas:
                self.tree.insert('', tk.END, values=(
                    escola['id_escola'],
                    escola['nome'],
                    escola['endereco'] or 'N/A',
                    escola['telefone'] or 'N/A',
                    escola['diretor'] or 'N/A',
                    escola['total_turmas']
                ))
            
            self.count_label.config(text=f"Total: {len(escolas)} escolas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def salvar(self):
        if not self.entries['nome'].get():
            messagebox.showwarning("Atenção", "Nome é obrigatório!")
            return
        
        data = {
            'nome': self.entries['nome'].get(),
            'endereco': self.entries['endereco'].get() or None,
            'telefone': self.entries['telefone'].get() or None,
            'diretor': self.entries['diretor'].get() or None
        }
        
        try:
            if self.selected_id is None:
                self.dao.create(data)
                messagebox.showinfo("✓ Sucesso", "Escola cadastrada com sucesso!")
            else:
                self.dao.update(self.selected_id, data)
                messagebox.showinfo("✓ Sucesso", "Escola atualizada com sucesso!")
            
            self.limpar()
            self.load_data()
        except Exception as e:
            messagebox.showerror("✗ Erro", f"Erro ao salvar: {e}")
    
    def editar(self):
        if self.selected_id is None:
            messagebox.showwarning("Atenção", "Selecione uma escola na tabela!")
            return
        
        try:
            escola = self.dao.read(self.selected_id)
            if escola:
                self.entries['nome'].delete(0, tk.END)
                self.entries['nome'].insert(0, escola['nome'])
                
                self.entries['endereco'].delete(0, tk.END)
                self.entries['endereco'].insert(0, escola['endereco'] or '')
                
                self.entries['telefone'].delete(0, tk.END)
                self.entries['telefone'].insert(0, escola['telefone'] or '')
                
                self.entries['diretor'].delete(0, tk.END)
                self.entries['diretor'].insert(0, escola['diretor'] or '')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar escola: {e}")
    
    def deletar(self):
        if self.selected_id is None:
            messagebox.showwarning("Atenção", "Selecione uma escola na tabela!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente deletar esta escola?"):
            try:
                self.dao.delete(self.selected_id)
                messagebox.showinfo("✓ Sucesso", "Escola deletada com sucesso!")
                self.limpar()
                self.load_data()
            except Exception as e:
                messagebox.showerror("✗ Erro", f"Erro ao deletar: {e}")
    
    def buscar(self):
        nome = self.search_entry.get()
        
        if not nome:
            messagebox.showwarning("Atenção", "Digite um nome para buscar!")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            escolas = self.dao.buscar_por_nome(nome)
            
            if not escolas:
                messagebox.showinfo("Resultado", "Nenhuma escola encontrada!")
                self.count_label.config(text="Total: 0 escolas")
                return
            
            for escola in escolas:
                self.tree.insert('', tk.END, values=(
                    escola['id_escola'],
                    escola['nome'],
                    escola['endereco'] or 'N/A',
                    escola['telefone'] or 'N/A',
                    escola['diretor'] or 'N/A',
                    0  # Não temos o count aqui
                ))
            
            self.count_label.config(text=f"Total: {len(escolas)} escolas encontradas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {e}")
    
    def limpar(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        self.selected_id = None
        self.search_entry.delete(0, tk.END)
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_id = item['values'][0]