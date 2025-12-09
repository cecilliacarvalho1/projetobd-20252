from dao.base_dao import BaseDAO
from database.connection import db


class AlunoDAO(BaseDAO):
    
    def __init__(self):
        super().__init__('Aluno', 'id_aluno')
    
    def buscar_por_nome(self, nome):
        query = f"SELECT * FROM {self.table_name} WHERE nome LIKE %s"
        try:
            return db.execute_query(query, (f"%{nome}%",), fetch=True)
        except Exception as e:
            print(f"✗ Erro ao buscar: {e}")
            raise