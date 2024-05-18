--QUERIES do Projeto
--Projeto relatorio 1
select
    a.ra
    ,a.nome
    ,c.materia_id
    ,m.nome_materia
    ,c.semestre
    ,c.ano
    ,case 
        when c.nota is null 
        then 'Matéria ainda está sendo cursada.' 
        else TO_CHAR(c.nota) 
        end as Nota_Final
    ,c.status
from
    aluno a
left join cursando c on a.ra =  c.ra
left join materia m on c.materia_id = m.materia_id
where 1=1
    --caso nulo, todos os alunos serão incluídos no resultado da query
    and (:ra_aluno is null or a.ra = :ra_aluno)
order by a.ra asc
;

--Projeto Relatorio 2
select
    p.ra
    ,p.nome
    ,l.materia_id
    ,m.nome_materia
    ,l.semestre
    ,l.ano
    ,l.status
from
    professor p
left join leciona l on p.ra = l.ra_prof
left join materia m on l.materia_id = m.materia_id
where 1=1
    --caso nulo, todos os professores serão incluídos no resultado da query
    and (:ra_professor is null or p.ra = :ra_professor)
    and l.materia_id is not null
order by p.ra asc
;

--Projeto relatorio 3
select distinct
    a.ra
    ,a.nome
    ,a.email
    ,a.curso_id
    ,c.nome_curso
    ,c2.semestre
    ,c2.ano
    ,'Formado!' as Status
from 
    aluno a
join curso c on a.curso_id = c.curso_id
join cursando c2 on a.ra = c2.ra
where 1=1
    --subquery pra ver se foi aprovado nas materias do seu curso
    and not exists (
        select 
            1 
        from 
            matrizcurricular mc
        --puxa as materias da matriz do curso
        join materia m on mc.materia_id = m.materia_id
        --puxa materias que o aluno cursa/cursou
        left join cursando c on a.ra = c.ra and m.materia_id = c.materia_id
        where 1=1
            and mc.curso_id = a.curso_id 
            and (c.status is null or c.status != 'Aprovado')
    )
    --subquery pra retornar resultados que batam com o semestre e ano desejado
    and exists (
        select 
            1 
        from 
            cursando c
        where 1=1
            and c.ra = a.ra 
            and c.semestre = :semestre
            and c.ano = :ano         
    )
    --garante que o semestre e ano sejam os desejados
    and c2.semestre = :semestre
    and c2.ano = :ano
    ;

--Projeto relatorio 4
select
    d.nome_dept as nome_departamento
    ,p.nome as nome_professor_chefe
from
    departamento d
left join professor p on d.chefe_ra = p.ra
;

--Projeto relatorio 5
select
    a.nome as nome_aluno
    ,p.nome as nome_prof_orientador
    ,o.grupo_id
from orientador o
left join aluno a on o.aluno_ra = a.ra
left join professor p on o.prof_ra = p.ra
where 1=1
    and o.grupo_id in (
        select 
            grupo_id
        from 
            orientador
        group by
            grupo_id
        having 
            count(*) > 1
    )
order by o.grupo_id
;
