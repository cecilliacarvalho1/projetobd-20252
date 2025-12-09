import tkinter as tk
from tkinter import ttk, messagebox
from dao.relatorio_dao import RelatorioDAO

class RelatorioView:
    
    def __init__(self, parent):
        self.dao = RelatorioDAO()
        self.window = tk.Toplevel(parent)
        self.window.title("Relatório de Alunos Ativos")
        self.window.geometry("1000x600")
        self.window.configure(bg='#ecf0f1')
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        # Cabeçalho
        header = tk.Frame(self.window, bg='#8e44ad', relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X)
        
        tk.Label(header, 
                text="📊 Relatório: Alunos Ativos", 
                font=('Segoe UI', 16, 'bold'), 
                bg='#8e44ad', 
                fg='white', 
                pady=15).pack()
        
        # Container da Tabela
        container = tk.Frame(self.window, bg='#ecf0f1')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(container, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(container, orient=tk.HORIZONTAL)
        
        # Treeview (Tabela)
        self.tree = ttk.Treeview(container, 
                                yscrollcommand=scroll_y.set, 
                                xscrollcommand=scroll_x.set,
                                show="headings")
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Botão Fechar
        tk.Button(self.window, text="Fechar", command=self.window.destroy,
                 bg='#95a5a6', fg='white', font=('Segoe UI', 10, 'bold'),
                 pady=8).pack(pady=10)

    def load_data(self):
        try:
            dados = self.dao.listar_alunos_ativos()
            
            if not dados:
                messagebox.showinfo("Aviso", "A visualização não retornou nenhum dado.")
                return

            # Configurar Colunas Dinamicamente (baseado no retorno do banco)
            colunas = list(dados[0].keys())
            self.tree["columns"] = colunas
            
            for col in colunas:
                # Formata o título (ex: nome_aluno -> Nome Aluno)
                titulo = col.replace('_', ' ').title()
                self.tree.heading(col, text=titulo)
                # Ajusta largura baseada no tamanho do título
                largura = len(titulo) * 15
                self.tree.column(col, width=max(100, largura), anchor=tk.CENTER)
            
            # Inserir Dados
            for linha in dados:
                valores = [linha[col] for col in colunas]
                self.tree.insert("", tk.END, values=valores)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar relatório: {e}")