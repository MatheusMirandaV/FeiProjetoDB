from faker import Faker
import random
#unicode para manipulação categorização e normalização de strings, usada pra evitar que acentos fiquem não identificados no arquivo de output
import unicodedata

# inicializa o faker com a localidade pt_BR
fake = Faker('pt_BR')

# função para remover acentos de uma string
def remover_acentos(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return u"".join([c for c in nfkd if not unicodedata.combining(c)])

# função para gerar email com base no primeiro nome e sobrenome sem acentos
def gerar_email(nome):
    nome_sem_acentos = remover_acentos(nome).lower().split()
    email = f"{nome_sem_acentos[0][0]}{nome_sem_acentos[1]}@fei.com"
    return email

# gera dados para a tabela departamento
# cada departamento tem um nome, orçamento, prédio e chefe (chefe_ra)
def gerar_departamento():
    departamentos = [
        ('Computacao', 50000, 'Predio K', None),
        ('Engenharia', 30000, 'Predio J', None),
        ('Matematica', 40000, 'Predio I', None),
        ('Administracao', 15000, 'Predio A', None)
    ]
    inserts = []
    for dept in departamentos:  
        # na hora de gerar o comando insert, none's são NULLS
        chefe_ra = 'NULL' if dept[3] is None else f"'{dept[3]}'"
        inserts.append(f"INSERT INTO Departamento (nome_dept, Orcamento, Predio, chefe_ra) VALUES ('{dept[0]}', {dept[1]}, '{dept[2]}', {chefe_ra});")
    return inserts, departamentos

# gera dados para a tabela professor
# cada professor tem um RA, CPF, nome, email, salário e departamento
def gerar_professor():
    departamentos = ['Computacao', 'Engenharia', 'Matematica', 'Administracao']
    professores = []
    for i in range(1, 26):
        ra = f'RA{i:03d}'
        cpf = fake.cpf()
        nome = fake.name()
        email = gerar_email(nome)
        salario = random.randint(4000, 15000)
        dept = random.choice(departamentos)
        professores.append((ra, cpf, nome, email, salario, dept))
    inserts = []
    for prof in professores:
        inserts.append(f"INSERT INTO Professor (RA, CPF, Nome, Email, Salario, nome_dept) VALUES ('{prof[0]}', '{prof[1]}', '{remover_acentos(prof[2])}', '{prof[3]}', {prof[4]}, '{prof[5]}');")
    return inserts, professores

# gera dados para a tabela curso
# cada curso tem um ID, nome e departamento
def gerar_curso():
    cursos = [
        ('C001', 'Ciencia da Computacao', 'Computacao'),
        ('C002', 'Engenharia Mecanica', 'Engenharia'),
        ('C003', 'Engenharia de Producao', 'Engenharia'),
        ('C004', 'Administracao', 'Administracao'),
        ('C005', 'Matematica', 'Matematica'),
        ('C006', 'Engenharia Eletrica', 'Engenharia'),
        ('C007', 'Engenharia Civil', 'Engenharia'),
        ('C008', 'Engenharia Quimica', 'Engenharia'),
        ('C009', 'Engenharia de Controle e Automacao', 'Engenharia'),
        ('C010', 'Engenharia da Computacao', 'Computacao')
    ]
    inserts = []
    for curso in cursos:
        inserts.append(f"INSERT INTO Curso (curso_id, nome_curso, nome_dept) VALUES ('{curso[0]}', '{remover_acentos(curso[1])}', '{curso[2]}');")
    return inserts, cursos

# gera dados para a tabela aluno
# cada aluno tem um RA, CPF, nome, email e ID do curso
def gerar_aluno():
    cursos = ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'C010']
    alunos = []
    for i in range(1, 101):
        ra = f'A{i:04d}'
        cpf = fake.cpf()
        nome = fake.name()
        email = gerar_email(nome)
        curso_id = random.choice(cursos)
        alunos.append((ra, cpf, nome, email, curso_id))
    inserts = []
    for aluno in alunos:
        inserts.append(f"INSERT INTO Aluno (RA, CPF, Nome, Email, curso_id) VALUES ('{aluno[0]}', '{aluno[1]}', '{remover_acentos(aluno[2])}', '{aluno[3]}', '{aluno[4]}');")
    return inserts, alunos

# gera dados para a tabela matéria
# cada matéria tem um ID, nome, departamento e ID do curso
def gerar_materia():
    materias = [
        ('M1001', 'Banco de Dados', 'Computacao', 'C001'),
        ('M1002', 'Calculo I', 'Matematica', 'C005'),
        ('M1003', 'Engenharia de Software', 'Computacao', 'C001'),
        ('M1004', 'Algebra Linear', 'Matematica', 'C005'),
        ('M1005', 'Logistica', 'Administracao', 'C004'),
        ('M1006', 'Controle e Automacao', 'Engenharia', 'C002'),
        ('M1007', 'Programacao I', 'Computacao', 'C010'),
        ('M1008', 'Programacao II', 'Computacao', 'C001'),
        ('M1009', 'Fisica I', 'Engenharia', 'C002'),
        ('M1010', 'Fisica II', 'Engenharia', 'C002'),
        ('M1011', 'Quimica Geral', 'Engenharia', 'C008'),
        ('M1012', 'Termodinamica', 'Engenharia', 'C006'),
        ('M1013', 'Resistencia dos Materiais', 'Engenharia', 'C007'),
        ('M1014', 'Mecanica dos Fluidos', 'Engenharia', 'C009'),
        ('M1015', 'Redes de Computadores', 'Computacao', 'C010')
    ]
    inserts = []
    for materia in materias:
        inserts.append(f"INSERT INTO Materia (materia_id, nome_materia, nome_dept, curso_id) VALUES ('{materia[0]}', '{remover_acentos(materia[1])}', '{materia[2]}', '{materia[3]}');")
    return inserts, materias

# gera dados para a tabela cursando
# se a nota for maior que 5, o status é 'Aprovado', se menor que 5, 'Reprovado', se nota for NULL, status é 'Cursando'
# o ano deve bater com o ano do semestre
# sempre gera pelo menos 2 alunos aprovados em todas as matérias no semestre 2023-2, ano 2023
# sempre gera pelo menos 2 alunos aprovados em todas as matérias no semestre 2023-1, ano 2023
# sempre gera pelo menos 2 alunos aprovados em todas as matérias no semestre 2024-1, ano 2024
def gerar_cursando(alunos, matriz_curricular):
    cursando = []
    alunos_aprovados = random.sample(alunos, 6)  # selecionar 6 alunos que serão aprovados em todas as matérias
    alunos_especificos = [
        (alunos_aprovados[0], '2023-2', 2023),
        (alunos_aprovados[1], '2023-2', 2023),
        (alunos_aprovados[2], '2023-1', 2023),
        (alunos_aprovados[3], '2023-1', 2023),
        (alunos_aprovados[4], '2024-1', 2024),
        (alunos_aprovados[5], '2024-1', 2024),
    ]

    for aluno, semestre, ano in alunos_especificos:
        curso_id = aluno[4]
        materias_do_curso = [mat[1] for mat in matriz_curricular if mat[0] == curso_id]
        for materia_id in materias_do_curso:
            nota = 8.0
            status = 'Aprovado'
            cursando.append((aluno[0], materia_id, semestre, ano, nota, status))

    for aluno in alunos:
        if aluno not in alunos_aprovados:
            curso_id = aluno[4]
            materias_do_curso = [mat[1] for mat in matriz_curricular if mat[0] == curso_id]
            for materia_id in materias_do_curso:
                ano = random.randint(2023, 2024)
                semestre = f'{ano}-{random.randint(1, 2)}'
                nota = round(random.uniform(0, 10), 1) if random.choice([True, False]) else 'NULL'
                if nota != 'NULL':
                    status = 'Aprovado' if nota > 5 else 'Reprovado'
                else:
                    status = 'Cursando'
                cursando.append((aluno[0], materia_id, semestre, ano, nota, status))

    inserts = []
    for curs in cursando:
        nota_value = 'NULL' if curs[4] == 'NULL' else curs[4]
        inserts.append(f"INSERT INTO Cursando (RA, materia_id, Semestre, Ano, Nota, status) VALUES ('{curs[0]}', '{curs[1]}', '{curs[2]}', {curs[3]}, {nota_value}, '{curs[5]}');")
    return inserts

# gera dados para a tabela leciona
# se o semestre for 2024-1, o status é 'Ativo' pois é o semestre atual, caso contrário é 'Inativo'
# cada matéria deve ter no mínimo 1 e no máximo 2 professores no semestre atual
def gerar_leciona(materias):
    professores = [f'RA{i:03d}' for i in range(1, 26)]
    materias_ids = [materia[0] for materia in materias]
    leciona = []
    materias_semestre_atual = {materia: 0 for materia in materias_ids}  # contador para garantir no máximo 2 professores por matéria no semestre atual

    for materia_id in materias_ids:
        for _ in range(random.randint(1, 2)):  # garantir que cada matéria tenha no máximo 2 professores no semestre atual
            ra_prof = random.choice(professores)
            semestre = '2024-1'
            ano = 2024
            status = 'Ativo'
            leciona.append((ra_prof, materia_id, semestre, ano, status))
            materias_semestre_atual[materia_id] += 1

    for _ in range(30):
        ra_prof = random.choice(professores)
        materia_id = random.choice(materias_ids)
        ano = random.randint(2023, 2023)  # semestres anteriores
        semestre = f'{ano}-{random.randint(1, 2)}'
        status = 'Inativo'
        leciona.append((ra_prof, materia_id, semestre, ano, status))

    inserts = []
    for lec in leciona:
        inserts.append(f"INSERT INTO Leciona (RA_Prof, materia_id, Semestre, Ano, status) VALUES ('{lec[0]}', '{lec[1]}', '{lec[2]}', {lec[3]}, '{lec[4]}');")
    return inserts

# gera dados para a tabela orientador
# grupos de tcc têm no máximo 4 integrantes, e um professor pode orientar no máximo 3 grupos
def gerar_orientador():
    alunos = [f'A{i:04d}' for i in range(1, 101)]
    professores = [f'RA{i:03d}' for i in range(1, 26)]
    grupos = []
    orientadores = []
    grupo_id = 1

    for _ in range(25):
        num_integrantes = random.randint(1, 4)
        integrantes = random.sample(alunos, num_integrantes)
        alunos = [aluno for aluno in alunos if aluno not in integrantes]
        orientadores.append((integrantes, random.choice(professores), f'G{grupo_id:03d}'))
        grupo_id += 1

    inserts = []
    for ori in orientadores:
        for aluno_ra in ori[0]:
            inserts.append(f"INSERT INTO Orientador (aluno_ra, prof_ra, grupo_id) VALUES ('{aluno_ra}', '{ori[1]}', '{ori[2]}');")
    return inserts

# gera dados para a tabela matriz curricular
# cada curso tem exatamente 3 matérias que existem nos inserts gerados para a tabela materia
def gerar_matriz_curricular(cursos, materias):
    materias_por_curso = {
        'Computacao': ['M1001', 'M1003', 'M1007', 'M1008', 'M1015'],
        'Engenharia': ['M1006', 'M1009', 'M1010', 'M1011', 'M1012', 'M1013', 'M1014'],
        'Matematica': ['M1002', 'M1004'],
        'Administracao': ['M1005']
    }
    matriz_curricular = []

    for curso in cursos:
        curso_id, nome_curso, nome_dept = curso
        dept = nome_dept
        materias_validas = [m[0] for m in materias if m[2] == dept or m[2] == 'Matematica']
        if dept == 'Matematica':
            materias_validas += [m[0] for m in materias if m[2] == 'Computacao']
        materias_selecionadas = random.sample(materias_validas, 3)
        for materia in materias_selecionadas:
            matriz_curricular.append((curso_id, materia))

    inserts = []
    for mat in matriz_curricular:
        inserts.append(f"INSERT INTO MatrizCurricular (curso_id, materia_id) VALUES ('{mat[0]}', '{mat[1]}');")
    return inserts, matriz_curricular

# função para gerar os comandos de update dos chefes de departamento
def gerar_update_chefe_departamento(professores, departamentos):
    updates = []
    for dept in departamentos:
        # filtra os professores do departamento atual
        profs_dept = [prof for prof in professores if prof[5] == dept[0]]
        if profs_dept:
            # escolhe um professor aleatório do departamento para ser o chefe
            chefe = random.choice(profs_dept)[0]
            updates.append(f"UPDATE Departamento SET chefe_ra = '{chefe}' WHERE nome_dept = '{dept[0]}';")
    return updates

# função principal para gerar todos os dados e salvar em inserts.sql
def gerar_dados():
    with open('inserts.sql', 'w', encoding='utf-8') as f:
        # departamento
        f.write('-- Departamento\n')
        dept_inserts, departamentos = gerar_departamento()
        for insert in dept_inserts:
            f.write(insert + '\n')
        
        # professor
        f.write('-- Professor\n')
        prof_inserts, professores = gerar_professor()
        for insert in prof_inserts:
            f.write(insert + '\n')
        
        # atualiza chefes de departamento
        f.write('-- Atualiza Chefes de Departamento\n')
        update_inserts = gerar_update_chefe_departamento(professores, departamentos)
        for update in update_inserts:
            f.write(update + '\n')
        
        # curso
        f.write('-- Curso\n')
        curso_inserts, cursos = gerar_curso()
        for insert in curso_inserts:
            f.write(insert + '\n')
        
        # aluno
        f.write('-- Aluno\n')
        aluno_inserts, alunos = gerar_aluno()
        for insert in aluno_inserts:
            f.write(insert + '\n')
        
        # matéria
        f.write('-- Matéria\n')
        materia_inserts, materias = gerar_materia()
        for insert in materia_inserts:
            f.write(insert + '\n')
        
        # matriz curricular
        f.write('-- Matriz Curricular\n')
        matriz_inserts, matriz_curricular = gerar_matriz_curricular(cursos, materias)
        for insert in matriz_inserts:
            f.write(insert + '\n')
        
        # cursando
        f.write('-- Cursando\n')
        cursando_inserts = gerar_cursando(alunos, matriz_curricular)
        for insert in cursando_inserts:
            f.write(insert + '\n')
        
        # leciona
        f.write('-- Leciona\n')
        leciona_inserts = gerar_leciona(materias)
        for insert in leciona_inserts:
            f.write(insert + '\n')
        
        # orientador
        f.write('-- Orientador\n')
        orientador_inserts = gerar_orientador()
        for insert in orientador_inserts:
            f.write(insert + '\n')

if __name__ == "__main__":
    gerar_dados()
    print("dados gerados e salvos em 'inserts.sql'")
