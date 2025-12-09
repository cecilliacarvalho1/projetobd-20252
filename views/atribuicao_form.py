import tkinter as tk
from tkinter import ttk, messagebox

class AtribuicaoForm:
    
    def __init__(self, parent, dao_aula, dao_disciplina, dao_professor, id_turma, callback=None):
        self.dao_aula = dao_aula
        self.dao_disciplina = dao_disciplina
        self.dao_professor = dao_professor
        self.id_turma = id_turma
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Nova Atribuição")
        self.window.geometry("500x400")
        self.window.configure(bg='#ecf0f1')
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.load_combos()
        self.create_widgets()
    
    def load_combos(self):
        # Carregar Disciplinas
        disciplinas = self.dao_disciplina.read_all()
        self.disciplinas_dict = {f"{d['nome']} ({d['carga_horaria']}h)": d['id_disciplina'] for d in disciplinas}
        
        # Carregar Professores Ativos
        professores = self.dao_professor.listar_ativos()
        self.professores_dict = {f"{p['nome']}": p['id_professor'] for p in professores}

    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg='#ffffff', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(main_frame, text="👨‍🏫 Atribuir Professor", font=('Segoe UI', 14, 'bold'), bg='#8e44ad', fg='white', pady=10)
        title.pack(fill=tk.X)
        
        fields_frame = tk.Frame(main_frame, bg='#ffffff')
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Disciplina
        tk.Label(fields_frame, text="Disciplina: *", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky=tk.W, pady=12)
        self.disciplina_var = tk.StringVar()
        disc_combo = ttk.Combobox(fields_frame, textvariable=self.disciplina_var, values=list(self.disciplinas_dict.keys()), state="readonly", width=35)
        disc_combo.grid(row=0, column=1, sticky=tk.W, pady=12, padx=(10, 0))
        
        # Professor
        tk.Label(fields_frame, text="Professor: *", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky=tk.W, pady=12)
        self.prof_var = tk.StringVar()
        prof_combo = ttk.Combobox(fields_frame, textvariable=self.prof_var, values=list(self.professores_dict.keys()), state="readonly", width=35)
        prof_combo.grid(row=1, column=1, sticky=tk.W, pady=12, padx=(10, 0))
        
        # Botão
        tk.Button(main_frame, text="💾 Confirmar Atribuição", command=self.salvar, bg='#8e44ad', fg='white', font=('Segoe UI', 10, 'bold'), padx=20, pady=10).pack(pady=20)

    def salvar(self):
        if not self.disciplina_var.get() or not self.prof_var.get():
            messagebox.showwarning("Atenção", "Selecione a disciplina e o professor!")
            return
            
        id_disciplina = self.disciplinas_dict[self.disciplina_var.get()]
        id_professor = self.professores_dict[self.prof_var.get()]
        
        try:
            # Chama o método que cria as aulas no banco
            self.dao_aula.atribuir_professor_disciplina(self.id_turma, id_disciplina, id_professor)
            messagebox.showinfo("Sucesso", "Professor atribuído com sucesso!")
            
            if self.callback:
                self.callback()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na atribuição: {e}")