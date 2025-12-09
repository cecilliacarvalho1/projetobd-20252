from database.connection import db

class RelatorioDAO:
    
    def listar_alunos_ativos(self):
        """Busca todos os dados da view de relatório"""
        query = "SELECT * FROM relatorio_alunos_ativos"
        try:
            # Retorna uma lista de dicionários
            return db.execute_query(query, fetch=True)
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            raise