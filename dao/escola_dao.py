from dao.base_dao import BaseDAO
from database.connection import db


class EscolaDAO(BaseDAO):
    
    def __init__(self):
        super().__init__('Escola', 'id_escola')
    
    def buscar_por_nome(self, nome):
        """
        Busca escolas por nome (busca parcial)
        
        Args:
            nome: Nome ou parte do nome
        
        Returns:
            Lista de escolas encontradas
        """
        return self.search('nome', nome, 'LIKE')
    
    def listar_com_turmas(self):
        """
        Lista escolas com quantidade de turmas
        
        Returns:
            Lista de escolas com informações de turmas
        """
        query = """
            SELECT 
                e.id_escola,
                e.nome,
                e.endereco,
                e.telefone,
                e.diretor,
                COUNT(t.id_turma) as total_turmas
            FROM Escola e
            LEFT JOIN Turma t ON e.id_escola = t.id_escola
            GROUP BY e.id_escola
            ORDER BY e.nome
        """
        
        try:
            return db.execute_query(query, fetch=True)
        except Exception as e:
            print(f"✗ Erro ao listar escolas: {e}")
            raise