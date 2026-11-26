
from mongo_cursos.conexao import obter_banco


# 1. Buscar cursos
def buscar_cursos(categoria=None, preco_max=None, tag=None):
    banco = obter_banco()

    filtros = {}

    if categoria:
        filtros["categoria"] = categoria

    if preco_max is not None:
        filtros["preco"] = {"$lte": preco_max}

    if tag:
        filtros["tags"] = tag

    return banco.cursos.find(filtros, {"modulos": 0})


# 2. Adicionar módulo
def adicionar_modulo(curso_id, modulo):
    banco = obter_banco()

    resultado = banco.cursos.update_one(
        {"_id": curso_id},
        {"$push": {"modulos": modulo}}
    )

    if resultado.matched_count > 0:
        print("Módulo adicionado com sucesso!")
    else:
        print("Curso não encontrado!")


# 3. Atualizar progresso
def atualizar_progresso(matricula_id, progresso):
    banco = obter_banco()

    if progresso < 0 or progresso > 100:
        print("Progresso inválido!")
        return

    resultado = banco.matriculas.update_one(
        {"_id": matricula_id},
        {
            "$set": {
                "progresso": progresso,
                "concluida": progresso == 100
            }
        }
    )

    if resultado.matched_count > 0:
        print("Progresso atualizado com sucesso!")
    else:
        print("Matrícula não encontrada!")


# 4. Remover aluno
def remover_aluno(aluno_id):
    banco = obter_banco()

    banco.matriculas.delete_many({"aluno_id": aluno_id})

    resultado = banco.alunos.delete_one({"_id": aluno_id})

    if resultado.deleted_count > 0:
        print("Aluno e suas matrículas foram removidos!")
    else:
        print("Aluno não encontrado!")
