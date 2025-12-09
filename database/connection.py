import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(**DB_CONFIG)
                print("✓ Conexão com MySQL OK!")
            return self._connection
        except Error as e:
            print(f"✗ Erro ao conectar: {e}")
            raise
    
    def disconnect(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("✓ Conexão encerrada")
    
    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            return self.connect()
        return self._connection
    
    def execute_query(self, query, params=None, fetch=False):
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                return cursor.lastrowid
                
        except Error as e:
            connection.rollback()
            print(f"✗ Erro ao executar query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()


db = DatabaseConnection()