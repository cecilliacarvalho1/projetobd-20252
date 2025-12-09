import tkinter as tk
from tkinter import ttk, messagebox


class MainWindow:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestão Escolar - UnB")
        self.root.geometry("900x650")
        
        # Cor de fundo moderna
        self.root.configure(bg='#1e3a5f')
        
        # Centralizar janela
        self.center_window()
        
        # Configurar estilo
        self.setup_style()
        
        self.create_widgets()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_style(self):
        """Configura cores e estilos modernos"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo dos botões principais
        style.configure('Menu.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=15,
                       background='#3498db',
                       foreground='white',
                       borderwidth=0)
        
        style.map('Menu.TButton',
                 background=[('active', '#2980b9')])
        
        # Estilo do botão sair
        style.configure('Exit.TButton',
                       font=('Segoe UI', 10),
                       padding=10,
                       background='#e74c3c',
                       foreground='white',
                       borderwidth=0)
        
        style.map('Exit.TButton',
                 background=[('active', '#c0392b')])
        
        # Estilo dos labels
        style.configure('Title.TLabel',
                       font=('Segoe UI', 26, 'bold'),
                       background='#1e3a5f',
                       foreground='white')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       background='#1e3a5f',
                       foreground='#bdc3c7')
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 10),
                       background='#34495e',
                       foreground='white')
    
    def create_widgets(self):
        # Container principal
        main_container = tk.Frame(self.root, bg='#1e3a5f')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # === CABEÇALHO ===
        header_frame = tk.Frame(main_container, bg='#1e3a5f')
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Título
        title = ttk.Label(header_frame,
                         text="🎓 Sistema de Gestão Escolar",
                         style='Title.TLabel')
        title.pack()
        
        # Subtítulo
        subtitle = ttk.Label(header_frame,
                            text="Universidade de Brasília - 2025/2",
                            style='Subtitle.TLabel')
        subtitle.pack(pady=(5, 0))
        
        # === MENU DE OPÇÕES ===
        menu_frame = tk.Frame(main_container, bg='#2c3e50', relief=tk.RAISED, bd=2)
        menu_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Título do menu
        menu_title = tk.Label(menu_frame,
                             text="Gerenciamento:",
                             font=('Segoe UI', 14, 'bold'),
                             bg='#34495e',
                             fg='white',
                             pady=15)
        menu_title.pack(fill=tk.X)
        
        # Container do botão
        buttons_container = tk.Frame(menu_frame, bg='#2c3e50')
        buttons_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=50)
        
        # Botão único para gerenciar escolas
        color = '#e67e22'
        btn = tk.Button(buttons_container,
                      text="🏫 Gerenciar Escolas",
                      command=self.abrir_escolas,
                      font=('Segoe UI', 16, 'bold'),
                      bg=color,
                      fg='white',
                      activebackground=self.darken_color(color),
                      activeforeground='white',
                      relief=tk.FLAT,
                      cursor='hand2',
                      padx=40,
                      pady=40,
                      borderwidth=0)
        
        btn.pack(expand=True)
        
        # Efeito hover
        btn.bind('<Enter>', lambda e: btn.configure(bg=self.lighten_color(color)))
        btn.bind('<Leave>', lambda e: btn.configure(bg=color))
        
        # === RODAPÉ ===
        footer_frame = tk.Frame(main_container, bg='#34495e', relief=tk.RAISED, bd=1)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        footer_text = ttk.Label(footer_frame,
                               text="Projeto de Banco de Dados | Departamento de Ciência da Computação",
                               style='Info.TLabel')
        footer_text.pack(pady=10)
        
        # Botão sair
        exit_btn = tk.Button(main_container,
                           text="🚪 Sair do Sistema",
                           command=self.sair,
                           font=('Segoe UI', 10, 'bold'),
                           bg='#e74c3c',
                           fg='white',
                           activebackground='#c0392b',
                           activeforeground='white',
                           relief=tk.FLAT,
                           cursor='hand2',
                           padx=30,
                           pady=10,
                           borderwidth=0)
        exit_btn.pack(pady=(10, 0))
    
    def lighten_color(self, color):
        """Clareia uma cor em hexadecimal"""
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def darken_color(self, color):
        """Escurece uma cor em hexadecimal"""
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def abrir_escolas(self):
        """Abre a tela de gerenciamento de escolas"""
        from views.escola_view_hierarquica import EscolaViewHierarquica
        EscolaViewHierarquica(self.root)
    
    def sair(self):
        """Fecha a aplicação"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.root.quit()
    
    def run(self):
        """Inicia o loop da interface"""
        self.root.mainloop()