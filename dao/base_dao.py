from database.connection import db


class BaseDAO:
    
    def __init__(self, table_name, id_column):
        self.table_name = table_name
        self.id_column = id_column
    
    def create(self, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            last_id = db.execute_query(query, tuple(data.values()))
            print(f"✓ Inserido em {self.table_name} ID: {last_id}")
            return last_id
        except Exception as e:
            print(f"✗ Erro ao inserir: {e}")
            raise
    
    def read(self, id_value):
        query = f"SELECT * FROM {self.table_name} WHERE {self.id_column} = %s"
        try:
            results = db.execute_query(query, (id_value,), fetch=True)
            return results[0] if results else None
        except Exception as e:
            print(f"✗ Erro ao buscar: {e}")
            raise
    
    def read_all(self):
        query = f"SELECT * FROM {self.table_name}"
        try:
            return db.execute_query(query, fetch=True)
        except Exception as e:
            print(f"✗ Erro ao listar: {e}")
            raise
    
    def update(self, id_value, data):
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.id_column} = %s"
        
        values = list(data.values())
        values.append(id_value)
        
        try:
            db.execute_query(query, tuple(values))
            print(f"✓ Atualizado em {self.table_name}")
            return True
        except Exception as e:
            print(f"✗ Erro ao atualizar: {e}")
            raise
    
    def delete(self, id_value):
        query = f"DELETE FROM {self.table_name} WHERE {self.id_column} = %s"
        try:
            db.execute_query(query, (id_value,))
            print(f"✓ Deletado de {self.table_name}")
            return True
        except Exception as e:
            print(f"✗ Erro ao deletar: {e}")
            raise