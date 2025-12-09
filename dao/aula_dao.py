from dao.base_dao import BaseDAO
from database.connection import db


class AulaDAO(BaseDAO):
    
    def __init__(self):
        super().__init__('Aula', 'id_aula')
    
    def listar_por_turma(self, id_turma):
        """
        Lista todas as disciplinas e professores de uma turma
        Agrupa para evitar duplicatas (mesma disciplina/professor várias aulas)
        
        Args:
            id_turma: ID da turma
        
        Returns:
            Lista com disciplinas, professores e carga horária
        """
        query = """
            SELECT 
                MIN(a.id_aula) as id_aula,
                a.id_turma,
                a.id_disciplina,
                a.id_professor,
                d.nome as disciplina_nome,
                d.carga_horaria,
                p.nome as professor_nome,
                p.formacao as professor_especialidade
            FROM Aula a
            INNER JOIN Disciplina d ON a.id_disciplina = d.id_disciplina
            INNER JOIN Professor p ON a.id_professor = p.id_professor
            WHERE a.id_turma = %s
            GROUP BY a.id_turma, a.id_disciplina, a.id_professor
            ORDER BY d.nome
        """
        
        try:
            return db.execute_query(query, (id_turma,), fetch=True)
        except Exception as e:
            print(f"✗ Erro ao listar disciplinas da turma: {e}")
            raise
    
    def verificar_atribuicao_existe(self, id_turma, id_disciplina, id_professor):
        """
        Verifica se já existe uma atribuição específica
        
        Args:
            id_turma: ID da turma
            id_disciplina: ID da disciplina
            id_professor: ID do professor
        
        Returns:
            True se existe, False caso contrário
        """
        query = """
            SELECT COUNT(*) as total 
            FROM Aula 
            WHERE id_turma = %s AND id_disciplina = %s AND id_professor = %s
        """
        
        try:
            result = db.execute_query(query, (id_turma, id_disciplina, id_professor), fetch=True)
            return result[0]['total'] > 0 if result else False
        except Exception as e:
            print(f"✗ Erro ao verificar atribuição: {e}")
            raise
    
    def atribuir_professor_disciplina(self, id_turma, id_disciplina, id_professor):
        """
        Atribui um professor a uma disciplina em uma turma
        Cria uma aula inicial como registro da atribuição
        
        Args:
            id_turma: ID da turma
            id_disciplina: ID da disciplina
            id_professor: ID do professor
        
        Returns:
            ID da aula criada
        """
        if self.verificar_atribuicao_existe(id_turma, id_disciplina, id_professor):
            raise Exception("Este professor já está atribuído a esta disciplina nesta turma!")
        
        # Criar uma aula "padrão" como registro da atribuição
        from datetime import date, time
        
        data = {
            'id_turma': id_turma,
            'id_disciplina': id_disciplina,
            'id_professor': id_professor,
            'data': date.today(),
            'hora_inicio': time(8, 0),
            'hora_fim': time(9, 0)
        }
        
        return self.create(data)
    
    def atualizar_professor(self, id_turma, id_disciplina, id_professor_novo):
        """
        Atualiza o professor de uma disciplina em uma turma
        Atualiza TODAS as aulas dessa disciplina nessa turma
        
        Args:
            id_turma: ID da turma
            id_disciplina: ID da disciplina
            id_professor_novo: Novo ID do professor
        
        Returns:
            True se atualizado com sucesso
        """
        query = """
            UPDATE Aula 
            SET id_professor = %s 
            WHERE id_turma = %s AND id_disciplina = %s
        """
        
        try:
            db.execute_query(query, (id_professor_novo, id_turma, id_disciplina))
            print(f"✓ Professor atualizado em Aula")
            return True
        except Exception as e:
            print(f"✗ Erro ao atualizar professor: {e}")
            raise
    
    def remover_atribuicao(self, id_turma, id_disciplina, id_professor):
        """
        Remove todas as aulas de um professor em uma disciplina de uma turma
        
        Args:
            id_turma: ID da turma
            id_disciplina: ID da disciplina
            id_professor: ID do professor
        
        Returns:
            True se removido com sucesso
        """
        query = """
            DELETE FROM Aula 
            WHERE id_turma = %s AND id_disciplina = %s AND id_professor = %s
        """
        
        try:
            db.execute_query(query, (id_turma, id_disciplina, id_professor))
            print(f"✓ Atribuição removida de Aula")
            return True
        except Exception as e:
            print(f"✗ Erro ao remover atribuição: {e}")
            raise