CREATE VIEW relatorio_alunos_ativos AS
SELECT
    A.nome AS Nome_Aluno,
    E.nome AS Nome_Escola,
    S.nome AS Nome_Serie,
    T.nome AS Nome_Turma,
    M.status AS Status_Matricula
FROM
    Aluno A
JOIN
    Matricula M ON A.id_aluno = M.id_aluno
JOIN
    Turma T ON M.id_turma = T.id_turma
JOIN
    Escola E ON T.id_escola = E.id_escola
JOIN
    Serie S ON T.id_serie = S.id_serie
WHERE
    M.status = 'Ativo';