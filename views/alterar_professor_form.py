import tkinter as tk
from tkinter import ttk, messagebox

class AlterarProfessorForm:
    
    def __init__(self, parent, dao_aula, dao_professor, atribuicao, callback=None):
        self.dao_aula = dao_aula
        self.dao_professor = dao_professor
        self.atribuicao = atribuicao
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Alterar Professor")
        
        # AUMENTADO O TAMANHO DA JANELA PARA CABER OS BOTÕES
        self.window.geometry("600x550") 
        self.window.configure(bg='#ecf0f1')
        self.window.transient(parent)
        self.window.grab_set()
        
        # PERMITIR REDIMENSIONAR (CASO AINDA FIQUE CORTADO)
        self.window.resizable(True, True)
        
        self.load_combos_data()
        self.create_widgets()
    
    def load_combos_data(self):
        # Carregar dados da atribuição atual
        from database.connection import db
        
        query = """
            SELECT 
                d.nome as disciplina_nome,
                p.nome as professor_nome
            FROM Aula a
            INNER JOIN Disciplina d ON a.id_disciplina = d.id_disciplina
            INNER JOIN Professor p ON a.id_professor = p.id_professor
            WHERE a.id_turma = %s AND a.id_disciplina = %s AND a.id_professor = %s
            LIMIT 1
        """
        
        result = db.execute_query(query, (
            self.atribuicao['id_turma'],
            self.atribuicao['id_disciplina'],
            self.atribuicao['id_professor']
        ), fetch=True)
        
        if result:
            self.disciplina_nome = result[0]['disciplina_nome']
            self.professor_atual = result[0]['professor_nome']
        else:
            self.disciplina_nome = "Desconhecida"
            self.professor_atual = "Desconhecido"
        
        # Carregar professores ativos
        professores = self.dao_professor.listar_ativos()
        self.professores_dict = {f"{p['nome']} - {p['formacao'] or 'Sem formação'}": 
                                p['id_professor'] for p in professores}
    
    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg='#ffffff', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(main_frame,
                        text="✏️ Alterar Professor",
                        font=('Segoe UI', 14, 'bold'),
                        bg='#f39c12',
                        fg='white',
                        pady=10)
        title.pack(fill=tk.X)
        
        # --- BOTÕES NO RODAPÉ ---
        btn_frame = tk.Frame(main_frame, bg='#ffffff')
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
        
        tk.Button(btn_frame,
                 text="💾 Alterar",
                 command=self.salvar,
                 font=('Segoe UI', 10, 'bold'),
                 bg='#f39c12',
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 padx=30,
                 pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame,
                 text="❌ Cancelar",
                 command=self.window.destroy,
                 font=('Segoe UI', 10, 'bold'),
                 bg='#95a5a6',
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 padx=30,
                 pady=10).pack(side=tk.LEFT, padx=5)

        # --- CAMPOS DO FORMULÁRIO ---
        fields_frame = tk.Frame(main_frame, bg='#ffffff')
        fields_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Disciplina
        tk.Label(fields_frame, text="Disciplina:", font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#2c3e50', anchor='w').grid(row=0, column=0, sticky=tk.W, pady=15)
        tk.Label(fields_frame, text=self.disciplina_nome, font=('Segoe UI', 10), bg='#ecf0f1', fg='#2c3e50', anchor='w', relief=tk.FLAT, padx=10, pady=8).grid(row=0, column=1, sticky='ew', pady=15, padx=(10, 0))
        
        # Professor Atual
        tk.Label(fields_frame, text="Professor Atual:", font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#2c3e50', anchor='w').grid(row=1, column=0, sticky=tk.W, pady=15)
        tk.Label(fields_frame, text=self.professor_atual, font=('Segoe UI', 10), bg='#ffe6e6', fg='#c0392b', anchor='w', relief=tk.FLAT, padx=10, pady=8).grid(row=1, column=1, sticky='ew', pady=15, padx=(10, 0))
        
        # Novo Professor
        tk.Label(fields_frame, text="Novo Professor: *", font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#2c3e50', anchor='w').grid(row=2, column=0, sticky=tk.W, pady=15)
        self.professor_var = tk.StringVar()
        professor_combo = ttk.Combobox(fields_frame, textvariable=self.professor_var, values=list(self.professores_dict.keys()), state="readonly", font=('Segoe UI', 9), width=35)
        professor_combo.grid(row=2, column=1, sticky='ew', pady=15, padx=(10, 0))
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Info
        info_frame = tk.Frame(fields_frame, bg='#fff3cd', relief=tk.SOLID, bd=1)
        info_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=15)
        
        tk.Label(info_frame,
                text="⚠️ Esta ação irá alterar o professor em TODAS as aulas\n"
                     "desta disciplina nesta turma.",
                font=('Segoe UI', 9),
                bg='#fff3cd',
                fg='#856404',
                justify=tk.LEFT,
                padx=10,
                pady=8).pack()
    
    def salvar(self):
        if not self.professor_var.get():
            messagebox.showwarning("Atenção", "Selecione o novo professor!")
            return
        
        id_professor_novo = self.professores_dict[self.professor_var.get()]
        
        if id_professor_novo == self.atribuicao['id_professor']:
            messagebox.showwarning("Atenção", "Você selecionou o mesmo professor!")
            return
        
        try:
            self.dao_aula.atualizar_professor(
                self.atribuicao['id_turma'],
                self.atribuicao['id_disciplina'],
                id_professor_novo
            )
            messagebox.showinfo("Sucesso", "Professor alterado com sucesso!")
            
            if self.callback:
                self.callback()
            
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar: {e}")