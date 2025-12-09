from dao.base_dao import BaseDAO
from database.connection import db


class TurmaDAO(BaseDAO):
    
    def __init__(self):
        super().__init__('Turma', 'id_turma')
    
    def listar_completo(self):
        """
        Lista turmas com informações de escola e série
        
        Returns:
            Lista de turmas com dados relacionados
        """
        query = """
            SELECT 
                t.id_turma,
                t.nome as turma_nome,
                t.turno,
                t.ano_letivo,
                t.capacidade,
                e.nome as escola_nome,
                s.nome as serie_nome,
                s.nivel as serie_nivel,
                COUNT(m.id_matricula) as total_alunos
            FROM Turma t
            INNER JOIN Escola e ON t.id_escola = e.id_escola
            INNER JOIN Serie s ON t.id_serie = s.id_serie
            LEFT JOIN Matricula m ON t.id_turma = m.id_turma AND m.status = 'Ativo'
            GROUP BY t.id_turma
            ORDER BY e.nome, s.nome, t.nome
        """
        
        try:
            return db.execute_query(query, fetch=True)
        except Exception as e:
            print(f"✗ Erro ao listar turmas: {e}")
            raise
    
    def buscar_por_escola(self, id_escola):
        """
        Busca turmas de uma escola específica
        """
        return self.search('id_escola', id_escola)