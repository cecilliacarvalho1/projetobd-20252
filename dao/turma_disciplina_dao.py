from dao.base_dao import BaseDAO
from database.connection import db


class TurmaDisciplinaDAO(BaseDAO):
    
    def __init__(self):
        super().__init__('Turma_Disciplina', 'id_turma_disciplina')
    
    def listar_por_turma(self, id_turma):
        """
        Lista todas as disciplinas e professores de uma turma
        
        Args:
            id_turma: ID da turma
        
        Returns:
            Lista com disciplinas, professores e carga horária
        """
        query = """
            SELECT 
                td.id_turma_disciplina,
                td.id_turma,
                td.id_disciplina,
                td.id_professor,
                d.nome as disciplina_nome,
                d.carga_horaria,
                p.nome as professor_nome,
                p.especialidade as professor_especialidade
            FROM Turma_Disciplina td
            INNER JOIN Disciplina d ON td.id_disciplina = d.id_disciplina
            INNER JOIN Professor p ON td.id_professor = p.id_professor
            WHERE td.id_turma = %s
            ORDER BY d.nome
        """
        
        try:
            return db.execute_query(query, (id_turma,), fetch=True)
        except Exception as e:
            print(f"✗ Erro ao listar disciplinas da turma: {e}")
            raise
    
    def verificar_duplicata(self, id_turma, id_disciplina):
        """
        Verifica se já existe uma atribuição de disciplina para a turma
        
        Args:
            id_turma: ID da turma
            id_disciplina: ID da disciplina
        
        Returns:
            True se existe duplicata, False caso contrário
        """
        query = """
            SELECT COUNT(*) as total 
            FROM Turma_Disciplina 
            WHERE id_turma = %s AND id_disciplina = %s
        """
        
        try:
            result = db.execute_query(query, (id_turma, id_disciplina), fetch=True)
            return result[0]['total'] > 0 if result else False
        except Exception as e:
            print(f"✗ Erro ao verificar duplicata: {e}")
            raise
    
    def atribuir_professor_disciplina(self, id_turma, id_disciplina, id_professor):
        """
        Atribui um professor a uma disciplina em uma turma
        
        Args:
            id_turma: ID da turma
            id_disciplina: ID da disciplina
            id_professor: ID do professor
        
        Returns:
            ID da atribuição criada
        """
        if self.verificar_duplicata(id_turma, id_disciplina):
            raise Exception("Esta disciplina já está atribuída a esta turma!")
        
        data = {
            'id_turma': id_turma,
            'id_disciplina': id_disciplina,
            'id_professor': id_professor
        }
        
        return self.create(data)
    
    def atualizar_professor(self, id_turma_disciplina, id_professor):
        """
        Atualiza o professor de uma atribuição existente
        
        Args:
            id_turma_disciplina: ID da atribuição
            id_professor: Novo ID do professor
        
        Returns:
            True se atualizado com sucesso
        """
        return self.update(id_turma_disciplina, {'id_professor': id_professor})