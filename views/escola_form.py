import tkinter as tk
from tkinter import messagebox


class EscolaForm:
    
    def __init__(self, parent, dao, escola=None, callback=None):
        self.dao = dao
        self.escola = escola
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Escola - Cadastro/Edição")
        self.window.geometry("500x400")
        self.window.configure(bg='#ecf0f1')
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.create_widgets()
        
        if escola:
            self.load_data()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg='#ffffff', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(main_frame,
                        text="📝 Dados da Escola",
                        font=('Segoe UI', 14, 'bold'),
                        bg='#e67e22',
                        fg='white',
                        pady=10)
        title.pack(fill=tk.X)
        
        fields_frame = tk.Frame(main_frame, bg='#ffffff')
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.entries = {}
        fields = [
            ("Nome da Escola:", "nome", True),
            ("Endereço:", "endereco", False),
            ("Telefone:", "telefone", False),
            ("Diretor(a):", "diretor", False),
        ]
        
        for i, (label_text, field_name, required) in enumerate(fields):
            label_txt = f"{label_text} {'*' if required else ''}"
            tk.Label(fields_frame,
                    text=label_txt,
                    font=('Segoe UI', 10, 'bold'),
                    bg='#ffffff',
                    fg='#2c3e50',
                    anchor='w').grid(row=i, column=0, sticky=tk.W, pady=12)
            
            entry = tk.Entry(fields_frame,
                           font=('Segoe UI', 10),
                           relief=tk.FLAT,
                           bg='#ecf0f1',
                           width=35,
                           bd=2)
            entry.grid(row=i, column=1, sticky=tk.W, pady=12, padx=(10, 0))
            self.entries[field_name] = entry
        
        tk.Label(fields_frame,
                text="* Campos obrigatórios",
                font=('Segoe UI', 8, 'italic'),
                bg='#ffffff',
                fg='#7f8c8d').grid(row=len(fields), column=0, columnspan=2, pady=5)
        
        btn_frame = tk.Frame(main_frame, bg='#ffffff')
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Button(btn_frame,
                 text="💾 Salvar",
                 command=self.salvar,
                 font=('Segoe UI', 10, 'bold'),
                 bg='#27ae60',
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
    
    def load_data(self):
        """Carrega dados da escola para edição"""
        self.entries['nome'].insert(0, self.escola['nome'])
        self.entries['endereco'].insert(0, self.escola['endereco'] or '')
        self.entries['telefone'].insert(0, self.escola['telefone'] or '')
        self.entries['diretor'].insert(0, self.escola['diretor'] or '')
    
    def salvar(self):
        nome = self.entries['nome'].get().strip()
        
        if not nome:
            messagebox.showwarning("Atenção", "O nome da escola é obrigatório!")
            return
        
        data = {
            'nome': nome,
            'endereco': self.entries['endereco'].get().strip() or None,
            'telefone': self.entries['telefone'].get().strip() or None,
            'diretor': self.entries['diretor'].get().strip() or None
        }
        
        try:
            if self.escola:
                self.dao.update(self.escola['id_escola'], data)
                messagebox.showinfo("Sucesso", "Escola atualizada com sucesso!")
            else:
                self.dao.create(data)
                messagebox.showinfo("Sucesso", "Escola cadastrada com sucesso!")
            
            if self.callback:
                self.callback()
            
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")