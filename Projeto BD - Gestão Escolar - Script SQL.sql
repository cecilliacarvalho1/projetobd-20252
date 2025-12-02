CREATE database ESCOLAS;
USE ESCOLAS;
CREATE TABLE Escola(
	id_escola integer PRIMARY KEY AUTO_INCREMENT,
	nome varchar(60) NOT NULL,
	endereco varchar(200),
	telefone varchar(13) UNIQUE,
	diretor varchar(50)
    );

CREATE TABLE Serie(
	id_serie integer PRIMARY KEY AUTO_INCREMENT,
	nome ENUM ('1º ano', '2º ano', '3º ano','4º ano', '5º ano', '6º ano', '7º ano', '8º ano', '9º ano') NOT NULL,
	nivel ENUM ('Ensino Fundamental 1', 'Ensino Fundamental 2') NOT NULL
    );

CREATE TABLE Turma(
	id_turma integer PRIMARY KEY AUTO_INCREMENT,
	id_escola integer,
	id_serie integer,
	nome ENUM ('A', 'B', 'C', 'D', 'E') NOT NULL,
	turno ENUM ('Matutino', 'Vespertino') NOT NULL,
	ano_letivo integer,
	capacidade integer,
	FOREIGN KEY (id_escola) REFERENCES escola(id_escola),
	FOREIGN KEY (id_serie) REFERENCES serie(id_serie)
    );

CREATE TABLE Aluno(
	id_aluno integer PRIMARY KEY AUTO_INCREMENT,
	nome varchar(100) NOT NULL,
	cpf char(11) UNIQUE,
	sexo ENUM ('Feminino', 'Masculino') NOT NULL,
	endereco varchar(200),
	telefone varchar(13) NOT NULL,
	email varchar(50),
	data_nascimento date NOT NULL,
	data_cadastro date,
	status ENUM ('Ativo', 'Inativo') NOT NULL
    );

CREATE TABLE Matricula(
	id_matricula integer PRIMARY KEY AUTO_INCREMENT,
	id_aluno integer,
	id_turma integer,
	ano_letivo integer,
	status ENUM ('Ativo', 'Inativo') NOT NULL,
	data_matricula date NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
    );
    
CREATE TABLE Disciplina(
	id_disciplina integer PRIMARY KEY AUTO_INCREMENT,
	nome ENUM ('Artes', 'Ciências', 'Educação Física', 'Geografia', 'História', 'Inglês', 'Matemática', 'Português') NOT NULL,
	carga_horaria time NOT NULL);

CREATE TABLE Avaliacao(
	id_avaliacao integer PRIMARY KEY AUTO_INCREMENT,
	id_matricula integer,
	id_disciplina integer,
	tipo ENUM ('Atividade', 'Prova', 'Trabalho') NOT NULL,
	data date,
	nota decimal (4, 2) NOT NULL CHECK (nota >= 0 AND nota <= 10),
    FOREIGN KEY (id_matricula) REFERENCES matricula(id_matricula),
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina)
    );

CREATE TABLE Professor(
	id_professor integer PRIMARY KEY AUTO_INCREMENT,
	nome varchar (50) NOT NULL,
	cpf char(11) UNIQUE,
	data_nascimento date,
	telefone varchar(13) NOT NULL,
	email varchar(50),
	formacao varchar(100) NOT NULL,
	data_admissao date NOT NULL,
	status ENUM ('Ativo', 'Inativo') NOT NULL
    );

CREATE TABLE Aula(
	id_aula integer PRIMARY KEY AUTO_INCREMENT,
	id_turma integer,
	id_disciplina integer,
	id_professor integer,
	data date NOT NULL,
	hora_inicio time NOT NULL,
	hora_fim time NOT NULL,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma),
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina),
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
    );

CREATE TABLE Responsavel(
	id_resp integer PRIMARY KEY AUTO_INCREMENT,
	nome varchar (50) NOT NULL,
	cpf char(11) UNIQUE,
	telefone varchar(13) NOT NULL,
	email varchar(50),
	endereco varchar(200),
	parentesco ENUM ('Avó/Avô', 'Irmã/Irmão', 'Mãe/Pai', 'Tia/Tio') NOT NULL
    );

CREATE TABLE Frequencia(
	id_frequencia integer PRIMARY KEY AUTO_INCREMENT,
	id_matricula integer,
	id_aula integer,
	presente ENUM ('Sim', 'Não') NOT NULL,
	data date NOT NULL,
    FOREIGN KEY (id_matricula) REFERENCES matricula(id_matricula),
    FOREIGN KEY (id_aula) REFERENCES aula(id_aula)
    );