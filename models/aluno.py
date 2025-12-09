from datetime import date


class Aluno:
    
    def __init__(self, id_aluno=None, nome='', cpf='', sexo='', 
                 endereco='', telefone='', email='', 
                 data_nascimento=None, data_cadastro=None, status='Ativo'):
        self.id_aluno = id_aluno
        self.nome = nome
        self.cpf = cpf
        self.sexo = sexo
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.data_nascimento = data_nascimento
        self.data_cadastro = data_cadastro or date.today()
        self.status = status
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'cpf': self.cpf,
            'sexo': self.sexo,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email,
            'data_nascimento': self.data_nascimento,
            'data_cadastro': self.data_cadastro,
            'status': self.status
        }