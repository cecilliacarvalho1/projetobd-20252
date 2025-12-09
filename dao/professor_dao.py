from dao.base_dao import BaseDAO
from database.connection import db


class ProfessorDAO(BaseDAO):
    
    def __init__(self):
        super().__init__('Professor', 'id_professor')
    
    def buscar_por_nome(self, nome):
        """
        Busca professores por nome (busca parcial)
        
        Args:
            nome: Nome ou parte do nome
        
        Returns:
            Lista de professores encontrados
        """
        query = f"SELECT * FROM {self.table_name} WHERE nome LIKE %s"
        try:
            return db.execute_query(query, (f"%{nome}%",), fetch=True)
        except Exception as e:
            print(f"✗ Erro ao buscar: {e}")
            raise
    
    def listar_ativos(self):
        """
        Lista apenas professores ativos
        
        Returns:
            Lista de professores ativos
        """
        query = f"SELECT * FROM {self.table_name} WHERE status = 'Ativo' ORDER BY nome"
        try:
            return db.execute_query(query, fetch=True)
        except Exception as e:
            print(f"✗ Erro ao listar professores ativos: {e}")
            raise