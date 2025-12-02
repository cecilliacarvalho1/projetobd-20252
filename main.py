import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tkinter import messagebox
from database.connection import db
from views.main_window import MainWindow


def main():
    try:
        db.connect()
        print("=" * 50)
        print("Sistema de Gestão Escolar")
        print("=" * 50)
        
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Erro: {e}")
        messagebox.showerror("Erro", f"Erro ao iniciar: {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()