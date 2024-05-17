--criando tabelas com as pk's primeiro, fk's são adicionadas posteriormente
CREATE TABLE Departamento(
    nome_dept VARCHAR2(255) PRIMARY KEY,
    Orcamento NUMBER(12, 2),
    Predio VARCHAR2(255),
    chefe_ra VARCHAR2(255)
);

CREATE TABLE Professor (
    RA VARCHAR2(255) PRIMARY KEY,
    CPF VARCHAR2(14) UNIQUE,
    Nome VARCHAR2(255),
    Email VARCHAR2(255),
    Salario NUMBER(10, 2),
    nome_dept VARCHAR2(255)
);

CREATE TABLE Curso (
    curso_id VARCHAR2(255) PRIMARY KEY,
    nome_curso VARCHAR2(255),
    nome_dept VARCHAR2(255)
);

CREATE TABLE Aluno (
    RA VARCHAR2(255) PRIMARY KEY,
    CPF VARCHAR2(14) UNIQUE,
    Nome VARCHAR2(255),
    Email VARCHAR2(255),
    curso_id VARCHAR2(255)
);

CREATE TABLE Materia (
    materia_id VARCHAR2(255) PRIMARY KEY,
    nome_materia VARCHAR2(255),
    nome_dept VARCHAR2(255),
    curso_id VARCHAR2(255)
);

CREATE TABLE Cursando (
    RA VARCHAR2(255),
    materia_id VARCHAR2(255),
    Semestre VARCHAR2(255),
    Ano NUMBER(4),
    Nota NUMBER,
    status VARCHAR2(255),
    PRIMARY KEY (RA, materia_id, Semestre, Ano)
);

CREATE TABLE Leciona (
    RA_Prof VARCHAR2(255),
    materia_id VARCHAR2(255),
    Semestre VARCHAR2(255),
    Ano NUMBER(4),
    status VARCHAR2(255),
    PRIMARY KEY (RA_Prof, materia_id, Semestre, Ano)
);

CREATE TABLE Orientador (
    aluno_ra VARCHAR2(255),
    prof_ra VARCHAR2(255),
    grupo_id VARCHAR2(255),
    PRIMARY KEY (aluno_ra, prof_ra)
);

CREATE TABLE MatrizCurricular (
    curso_id VARCHAR2(255),
    materia_id VARCHAR2(255),
    PRIMARY KEY (curso_id, materia_id)
);

-- adiciona fk's
ALTER TABLE Departamento ADD CONSTRAINT fk_dept_prof FOREIGN KEY (chefe_ra) REFERENCES Professor(RA) ON DELETE CASCADE;
ALTER TABLE Professor ADD CONSTRAINT fk_prof_dept FOREIGN KEY (nome_dept) REFERENCES Departamento(nome_dept) ON DELETE CASCADE;
ALTER TABLE Curso ADD CONSTRAINT fk_curso_dept FOREIGN KEY (nome_dept) REFERENCES Departamento(nome_dept) ON DELETE CASCADE;
ALTER TABLE Aluno ADD CONSTRAINT fk_aluno_curso FOREIGN KEY (curso_id) REFERENCES Curso(curso_id) ON DELETE CASCADE;
ALTER TABLE Materia ADD CONSTRAINT fk_materia_dept FOREIGN KEY (nome_dept) REFERENCES Departamento(nome_dept) ON DELETE CASCADE;
ALTER TABLE Materia ADD CONSTRAINT fk_materia_curso FOREIGN KEY (curso_id) REFERENCES Curso(curso_id) ON DELETE CASCADE;
ALTER TABLE Cursando ADD CONSTRAINT fk_cursando_aluno FOREIGN KEY (RA) REFERENCES Aluno(RA) ON DELETE CASCADE;
ALTER TABLE Cursando ADD CONSTRAINT fk_cursando_materia FOREIGN KEY (materia_id) REFERENCES Materia(materia_id) ON DELETE CASCADE;
ALTER TABLE Leciona ADD CONSTRAINT fk_leciona_prof FOREIGN KEY (RA_Prof) REFERENCES Professor(RA) ON DELETE CASCADE;
ALTER TABLE Leciona ADD CONSTRAINT fk_leciona_materia FOREIGN KEY (materia_id) REFERENCES Materia(materia_id) ON DELETE CASCADE;
ALTER TABLE Orientador ADD CONSTRAINT fk_orientador_aluno FOREIGN KEY (aluno_ra) REFERENCES Aluno(RA) ON DELETE CASCADE;
ALTER TABLE Orientador ADD CONSTRAINT fk_orientador_prof FOREIGN KEY (prof_ra) REFERENCES Professor(RA) ON DELETE CASCADE;
ALTER TABLE MatrizCurricular ADD CONSTRAINT fk_matriz_curso FOREIGN KEY (curso_id) REFERENCES Curso(curso_id) ON DELETE CASCADE;
ALTER TABLE MatrizCurricular ADD CONSTRAINT fk_matriz_materia FOREIGN KEY (materia_id) REFERENCES Materia(materia_id) ON DELETE CASCADE;