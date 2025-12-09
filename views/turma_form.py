import tkinter as tk
from tkinter import ttk, messagebox
from dao.escola_dao import EscolaDAO
from database.connection import db

class TurmaForm:
    
    def __init__(self, parent, dao, id_escola=None, turma=None, callback=None):
        self.dao = dao
        self.id_escola = id_escola
        self.turma = turma
        self.callback = callback
        self.dao_escola = EscolaDAO()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Turma - Cadastro/Edição")
        self.window.geometry("500x550")
        self.window.configure(bg='#ecf0f1')
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.create_widgets()
        
        if turma:
            self.load_data()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg='#ffffff', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(main_frame,
                        text="📚 Dados da Turma",
                        font=('Segoe UI', 14, 'bold'),
                        bg='#1abc9c',
                        fg='white',
                        pady=10)
        title.pack(fill=tk.X)
        
        fields_frame = tk.Frame(main_frame, bg='#ffffff')
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Série
        tk.Label(fields_frame, text="Série: *", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky=tk.W, pady=10)
        
        query = "SELECT id_serie, nome, nivel FROM Serie ORDER BY id_serie"
        series = db.execute_query(query, fetch=True)
        self.series_dict = {f"{s['nome']} - {s['nivel']}": s['id_serie'] for s in series}
        
        self.serie_var = tk.StringVar()
        serie_combo = ttk.Combobox(fields_frame, textvariable=self.serie_var, values=list(self.series_dict.keys()), state="readonly", width=33)
        serie_combo.grid(row=0, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Nome da Turma
        tk.Label(fields_frame, text="Sigla (A, B...): *", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky=tk.W, pady=10)
        
        self.nome_var = tk.StringVar(value="A")
        nome_combo = ttk.Combobox(fields_frame, textvariable=self.nome_var, values=["A", "B", "C", "D", "E"], state="readonly", width=33)
        nome_combo.grid(row=1, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Turno
        tk.Label(fields_frame, text="Turno: *", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=2, column=0, sticky=tk.W, pady=10)
        
        self.turno_var = tk.StringVar(value="Matutino")
        turno_combo = ttk.Combobox(fields_frame, textvariable=self.turno_var, values=["Matutino", "Vespertino", "Noturno"], state="readonly", width=33)
        turno_combo.grid(row=2, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Ano Letivo
        tk.Label(fields_frame, text="Ano Letivo: *", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=3, column=0, sticky=tk.W, pady=10)
        self.ano_entry = tk.Entry(fields_frame, relief=tk.FLAT, bg='#ecf0f1', width=35, bd=2)
        self.ano_entry.insert(0, "2025")
        self.ano_entry.grid(row=3, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Capacidade
        tk.Label(fields_frame, text="Capacidade: *", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=4, column=0, sticky=tk.W, pady=10)
        self.capacidade_entry = tk.Entry(fields_frame, relief=tk.FLAT, bg='#ecf0f1', width=35, bd=2)
        self.capacidade_entry.insert(0, "30")
        self.capacidade_entry.grid(row=4, column=1, sticky=tk.W, pady=10, padx=(10, 0))
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg='#ffffff')
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Button(btn_frame, text="💾 Salvar", command=self.salvar, bg='#1abc9c', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy, bg='#95a5a6', fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=8).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        if self.turma:
            for key, value in self.series_dict.items():
                if value == self.turma['id_serie']: # Ajuste se necessário para acessar dict ou objeto
                    self.serie_var.set(key)
                    break
            
            # Verifica se turma é dict ou objeto, ajusta conforme DAO retorna
            nome = self.turma.get('turma_nome') if isinstance(self.turma, dict) else self.turma['nome']
            turno = self.turma.get('turno')
            ano = self.turma.get('ano_letivo')
            cap = self.turma.get('capacidade')
            
            self.nome_var.set(nome)
            self.turno_var.set(turno)
            self.ano_entry.delete(0, tk.END)
            self.ano_entry.insert(0, str(ano))
            self.capacidade_entry.delete(0, tk.END)
            self.capacidade_entry.insert(0, str(cap))
            
            # Se estiver editando, usamos o id_escola da turma
            if 'id_escola' in self.turma:
                self.id_escola = self.turma['id_escola']

    def salvar(self):
        if not self.serie_var.get() or not self.nome_var.get():
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios!")
            return
            
        try:
            data = {
                'id_escola': self.id_escola,
                'id_serie': self.series_dict[self.serie_var.get()],
                'nome': self.nome_var.get(),
                'turno': self.turno_var.get(),
                'ano_letivo': int(self.ano_entry.get()),
                'capacidade': int(self.capacidade_entry.get())
            }
            
            if self.turma:
                # Se for edição, assume que self.turma tem id_turma
                id_turma = self.turma['id_turma']
                self.dao.update(id_turma, data)
                messagebox.showinfo("Sucesso", "Turma atualizada!")
            else:
                self.dao.create(data)
                messagebox.showinfo("Sucesso", "Turma criada!")
                
            if self.callback:
                self.callback()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")