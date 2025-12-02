SELECT * FROM escola
INSERT INTO escola(nome, endereco, telefone, diretor) VALUES ('Centro de Ensino Fundamental 1 do Núcleo Bandeirante', 'Terceira Avenida Bloco 1530 - Brasília/DF', '(61)3552-8732', 'João Souza')
INSERT INTO escola(nome, endereco, telefone, diretor) VALUES ('Centro Educacional Vale Verde', 'Rua das Montanhas, 400 - Belo Horizonte/MG', '(31)9982-3401', 'Cláudia Santos')
INSERT INTO escola(nome, endereco, telefone, diretor) VALUES ('Escola Municipal Primavera', 'Av. Independência, 522 - Goiânia/GO', '(62)3389-1144', 'Maria dos Anjos Carvalho')
INSERT INTO escola(nome, endereco, telefone, diretor) VALUES ('Escola São Gabriel', 'Rua Santo Antônio, 87 - São Paulo/SP', '(11)2598-4421', 'Bernardo Soares')
INSERT INTO escola(nome, endereco, telefone, diretor) VALUES ('Instituto Educacional Monte Azul', 'Rua Monte Alegre, 1780 - Rio de Janeiro/RJ', '(21)3033-2210', 'Marcos Silva')

SELECT * FROM serie
INSERT INTO serie(nome, nivel) VALUES ('1º ano', 'Ensino Fundamental 1')
INSERT INTO serie(nome, nivel) VALUES ('2º ano', 'Ensino Fundamental 1')
INSERT INTO serie(nome, nivel) VALUES ('3º ano', 'Ensino Fundamental 1')
INSERT INTO serie(nome, nivel) VALUES ('4º ano', 'Ensino Fundamental 1')
INSERT INTO serie(nome, nivel) VALUES ('5º ano', 'Ensino Fundamental 2')
INSERT INTO serie(nome, nivel) VALUES ('6º ano', 'Ensino Fundamental 2')
INSERT INTO serie(nome, nivel) VALUES ('7º ano', 'Ensino Fundamental 2')
INSERT INTO serie(nome, nivel) VALUES ('8º ano', 'Ensino Fundamental 2')
INSERT INTO serie(nome, nivel) VALUES ('9º ano', 'Ensino Fundamental 2')

SELECT * FROM turma
INSERT INTO turma(id_escola, id_serie, nome, turno, ano_letivo, capacidade) VALUES ('7', '8', 'A', 'Matutino', '2025', '40')
INSERT INTO turma(id_escola, id_serie, nome, turno, ano_letivo, capacidade) VALUES ('7', '8', 'B', 'Matutino', '2025', '38')
INSERT INTO turma(id_escola, id_serie, nome, turno, ano_letivo, capacidade) VALUES ('5', '9', 'D', 'Vespertino', '2025', '30')
INSERT INTO turma(id_escola, id_serie, nome, turno, ano_letivo, capacidade) VALUES ('4', '5', 'D', 'Vespertino', '2025', '22')
INSERT INTO turma(id_escola, id_serie, nome, turno, ano_letivo, capacidade) VALUES ('5', '9', 'C', 'Matutino', '2025', '32')

SELECT * FROM aluno
INSERT INTO aluno(nome, cpf, sexo, endereco, telefone, email, data_nascimento, data_cadastro, status) VALUES ('Henrique Menezes', '08754367588', 'Masculino', 'Rua Floriano Peixoto, 33 - Rio de Janeiro/RJ', '(21)8456-2382', 'henrique.menezes@hotmail.com', '2014-11-10', '2023-02-02', 'Ativo')
INSERT INTO aluno(nome, cpf, sexo, endereco, telefone, email, data_nascimento, data_cadastro, status) VALUES ('Mônica Santos', '84509823192', 'Feminino', 'Rua Carlito Teles, 658 - São Paulo/SP', '(11)9831-2342', '', '2013-05-03', '2020-02-14', 'Ativo')
INSERT INTO aluno(nome, cpf, sexo, endereco, telefone, email, data_nascimento, data_cadastro, status) VALUES ('Letícia Cabral', '00965348744', 'Feminino', 'Terceira Avenida Bloco 650 - Brasília/DF', '(61)9224-0674', '', '2014-12-02', '2020-02-13', 'Ativo')
INSERT INTO aluno(nome, cpf, sexo, endereco, telefone, email, data_nascimento, data_cadastro, status) VALUES ('Matheus Ribeiro', '09326377283', 'Masculino', 'Rua Independente, 1100 - Salvador/BA', '(71)9345-2738', '', '2014-12-19', '2020-02-13', 'Ativo')
INSERT INTO aluno(nome, cpf, sexo, endereco, telefone, email, data_nascimento, data_cadastro, status) VALUES ('Larissa Carvalho', '07265473888', 'Feminino', 'Avenida São Francisco de Assis - Belo Horizonte/MG', '(31)9987-3666', 'larissacarvalho01@gmail.com', '2006-07-08', '2016-03-03', 'Inativo')

SELECT * FROM matricula
INSERT INTO matricula(id_aluno, id_turma, ano_letivo, status, data_matricula) VALUES ('1', '1', '2025', 'Ativo', '2023-03-03')
INSERT INTO matricula(id_aluno, id_turma, ano_letivo, status, data_matricula) VALUES ('2', '5', '2025', 'Ativo', '2023-03-05')
INSERT INTO matricula(id_aluno, id_turma, ano_letivo, status, data_matricula) VALUES ('3', '1', '2025', 'Ativo', '2023-03-03')
INSERT INTO matricula(id_aluno, id_turma, ano_letivo, status, data_matricula) VALUES ('4', '2', '2025', 'Ativo', '2023-03-04')
INSERT INTO matricula(id_aluno, id_turma, ano_letivo, status, data_matricula) VALUES ('5', '5', '2025', 'Inativo', '2020-02-29')

SELECT * FROM disciplina
INSERT INTO disciplina(nome, carga_horaria) VALUES ('Ciências','100:00:00')
INSERT INTO disciplina(nome, carga_horaria) VALUES ('Matemática','200:00:00')
INSERT INTO disciplina(nome, carga_horaria) VALUES ('Português','200:00:00')
INSERT INTO disciplina(nome, carga_horaria) VALUES ('Inglês','100:00:00')
INSERT INTO disciplina(nome, carga_horaria) VALUES ('Artes','80:00:00')

SELECT * FROM avaliacao
INSERT INTO avaliacao(id_matricula, id_disciplina, tipo, data, nota) VALUES ('1', '1', 'Prova', '2025-11-19', '8.00')
INSERT INTO avaliacao(id_matricula, id_disciplina, tipo, data, nota) VALUES ('1', '2', 'Atividade', '2025-12-01', '0.70')
INSERT INTO avaliacao(id_matricula, id_disciplina, tipo, data, nota) VALUES ('2', '1', 'Prova', '2025-11-19', '6.75')
INSERT INTO avaliacao(id_matricula, id_disciplina, tipo, data, nota) VALUES ('3', '1', 'Prova', '2025-11-19', '5.20')
INSERT INTO avaliacao(id_matricula, id_disciplina, tipo, data, nota) VALUES ('4', '1', 'Prova', '2025-11-19', '7.80')

SELECT * FROM professor
INSERT INTO professor(nome, cpf, data_nascimento, telefone, email, formacao, data_admissao, status) VALUES ('Adriano Moreira', '98765439872', '1979-04-30', '(61)9854-4456', 'moreira_adriano@outlook.com', 'Doutorado em Matemática pela UFG', '2000-02-18', 'Ativo')
INSERT INTO professor(nome, cpf, data_nascimento, telefone, email, formacao, data_admissao, status) VALUES ('Jéssica Moura', '88836428392', '1982-03-02', '(71)8374-0039', 'jessicamoura123@gmail.com', 'Graduada em Artes pelo Instituto Federal de Salvador', '2022-06-30', 'Inativo')
INSERT INTO professor(nome, cpf, data_nascimento, telefone, email, formacao, data_admissao, status) VALUES ('Joyce Lima', '73636472833', '1983-07-24', '(21)8456-3827', 'lima.joyce@gmail.com', 'Doutorado em Inglês pela Faculdade de Letras do Rio de Janeiro', '2015-01-28', 'Ativo')
INSERT INTO professor(nome, cpf, data_nascimento, telefone, email, formacao, data_admissao, status) VALUES ('Marcos Rogério', '87634529304', '1975-10-16', '(61)9887-3219', 'marcosrogerio00@gmail.com', 'Mestrado em Português pela Universidade de Brasília', '2000-06-01', 'Ativo')
INSERT INTO professor(nome, cpf, data_nascimento, telefone, email, formacao, data_admissao, status) VALUES ('Daiane Lima', '06546729381', '1979-12-24', '(61)8564-3829', 'daianelimasantos@hotmail.com', 'Graduada em Artes pela Universidade Católica de Brasília', '2025-01-10', 'Ativo')

SELECT * FROM aula
INSERT INTO aula(id_turma, id_disciplina, id_professor, data, hora_inicio, hora_fim) VALUES ('1', '2', '1', '2025-11-24', '07:15:00', '09:00:00')
INSERT INTO aula(id_turma, id_disciplina, id_professor, data, hora_inicio, hora_fim) VALUES ('2', '2', '1', '2025-11-25', '09:15:00', '11:00:00')
INSERT INTO aula(id_turma, id_disciplina, id_professor, data, hora_inicio, hora_fim) VALUES ('3', '3', '4', '2025-11-26', '11:00:00', '12:15:00')
INSERT INTO aula(id_turma, id_disciplina, id_professor, data, hora_inicio, hora_fim) VALUES ('4', '4', '3', '2025-11-27', '13:00:00', '14:15:00')
INSERT INTO aula(id_turma, id_disciplina, id_professor, data, hora_inicio, hora_fim) VALUES ('5', '5', '5', '2025-11-28', '14:30:00', '16:00:00')

SELECT * FROM responsavel
INSERT INTO responsavel(nome, cpf, telefone, email, endereco, parentesco) VALUES ('Karina Santos', '98764358300', '(71)3552-4421', '', 'Rua Bandeirantes - Salvador/BA', 'Tia/Tio')
INSERT INTO responsavel(nome, cpf, telefone, email, endereco, parentesco) VALUES ('Jonathan Soares', '73848399976', '(21)9843-2173', '', 'Rua Olegário Maciel - Rio de Janeiro/RJ', 'Mãe/Pai')
INSERT INTO responsavel(nome, cpf, telefone, email, endereco, parentesco) VALUES ('Carmelita Silva', '34536273648', '(61)84756374', '', 'SQS 303 Norte - Brasília/DF', 'Avó/Avô')
INSERT INTO responsavel(nome, cpf, telefone, email, endereco, parentesco) VALUES ('Davi Dias', '47382938456', '(11)33867531', '', 'Avenida Brigadeiro Faria Lima - São Paulo/SP', 'Irmã/Irmão')
INSERT INTO responsavel(nome, cpf, telefone, email, endereco, parentesco) VALUES ('Douglas Amaral', '12845820293', '(31)99453617', '', 'Avenida Santa Luzia - Belo Horizonte/MG', 'Mãe/Pai')

SELECT * FROM frequencia
INSERT INTO frequencia(id_matricula, id_aula, presente, data) VALUES ('1', '1', 'Sim', '2025-11-24')
INSERT INTO frequencia(id_matricula, id_aula, presente, data) VALUES ('1', '2', 'Sim', '2025-11-25')
INSERT INTO frequencia(id_matricula, id_aula, presente, data) VALUES ('2', '3', 'Não', '2025-11-26')
INSERT INTO frequencia(id_matricula, id_aula, presente, data) VALUES ('2', '4', 'Sim', '2025-11-27')
INSERT INTO frequencia(id_matricula, id_aula, presente, data) VALUES ('3', '5', 'Sim', '2025-11-28')