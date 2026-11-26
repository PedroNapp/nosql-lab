
from mongo_cursos.conexao import obter_banco
from mongo_cursos.repositorio import buscar_cursos, atualizar_progresso


def formatar_data(data):
    ano, mes, dia = data.split("-")
    return dia + "/" + mes + "/" + ano


def converter_data(data):
    dia, mes, ano = data.split("/")
    return ano + "-" + mes + "-" + dia


def matricular_aluno():
    banco = obter_banco()

    email = input("Email do aluno: ")
    titulo = input("Titulo do curso: ")

    aluno = banco.alunos.find_one({"email": email})
    curso = banco.cursos.find_one({"titulo": titulo})

    if aluno is None:
        print("Aluno não encontrado!")
        return

    if curso is None:
        print("Curso não encontrado!")
        return

    matricula = banco.matriculas.find_one({
        "aluno_id": aluno["_id"],
        "curso_id": curso["_id"]
    })

    if matricula:
        print("Aluno já está matriculado neste curso!")
        return

    if curso["vagas"] <= 0:
        print("Curso sem vagas disponíveis!")
        return

    data = input("Data da matrícula (DD/MM/AAAA): ")

    try:
        data = converter_data(data)
    except ValueError:
        print("Data inválida! Utilize DD/MM/AAAA.")
        return

    banco.matriculas.insert_one({
        "aluno_id": aluno["_id"],
        "curso_id": curso["_id"],
        "data_matricula": data,
        "progresso": 0,
        "concluida": False,
        "nota": None
    })

    banco.cursos.update_one(
        {"_id": curso["_id"]},
        {"$set": {"vagas": curso["vagas"] - 1}}
    )

    print("Matrícula realizada com sucesso!")


def localizar_matricula(banco):
    email = input("Email do aluno: ")
    titulo = input("Titulo do curso: ")

    aluno = banco.alunos.find_one({"email": email})
    curso = banco.cursos.find_one({"titulo": titulo})

    if aluno is None or curso is None:
        print("Aluno ou curso não encontrado!")
        return None

    matricula = banco.matriculas.find_one({
        "aluno_id": aluno["_id"],
        "curso_id": curso["_id"]
    })

    if matricula is None:
        print("Matrícula não encontrada!")
        return None

    return matricula


def atualizar():
    banco = obter_banco()

    matricula = localizar_matricula(banco)

    if matricula is None:
        return

    progresso = int(input("Novo progresso (0 a 100): "))

    atualizar_progresso(matricula["_id"], progresso)


def avaliar():
    banco = obter_banco()

    matricula = localizar_matricula(banco)

    if matricula is None:
        return

    if matricula["progresso"] != 100:
        print("O aluno precisa concluir o curso para avaliar!")
        return

    nota = int(input("Digite uma nota de 1 a 5: "))

    if nota < 1 or nota > 5:
        print("Nota inválida!")
        return

    banco.matriculas.update_one(
        {"_id": matricula["_id"]},
        {"$set": {"nota": nota}}
    )

    print("Avaliação registrada com sucesso!")


def relatorio_cursos():
    banco = obter_banco()

    print("\n--- CURSOS E VAGAS ---")

    cursos = banco.cursos.find()

    for curso in cursos:
        print("Curso:", curso["titulo"])
        print("Categoria:", curso["categoria"])
        print("Vagas:", curso["vagas"])
        print("----------------------")


def relatorio_matriculas():
    banco = obter_banco()

    print("\n--- MATRICULAS POR CURSO ---")

    cursos = banco.cursos.find()

    for curso in cursos:
        total = 0

        matriculas = banco.matriculas.find({
            "curso_id": curso["_id"]
        })

        for matricula in matriculas:
            total += 1

        print("Curso:", curso["titulo"])
        print("Total de matriculas:", total)
        print("----------------------")


def relatorio_desempenho():
    banco = obter_banco()

    print("\n--- DESEMPENHO DOS ALUNOS ---")

    matriculas = banco.matriculas.find()

    for matricula in matriculas:
        aluno = banco.alunos.find_one({
            "_id": matricula["aluno_id"]
        })

        curso = banco.cursos.find_one({
            "_id": matricula["curso_id"]
        })

        if aluno and curso:
            print("\nAluno:", aluno["nome"])
            print("Email:", aluno["email"])
            print("Data de cadastro:", formatar_data(aluno["data_cadastro"]))
            print("Curso:", curso["titulo"])
            print("Data da matricula:", formatar_data(matricula["data_matricula"]))
            print("Progresso:", matricula["progresso"], "%")
            print("Nota:", matricula["nota"])
            print("----------------------")


def exibir_relatorios():
    relatorio_cursos()
    relatorio_matriculas()
    relatorio_desempenho()


def menu():
    while True:
        print("\n===== APRENDA+ =====")
        print("1 - Buscar cursos")
        print("2 - Matricular aluno")
        print("3 - Atualizar progresso")
        print("4 - Avaliar curso")
        print("5 - Exibir os tres relatorios")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            categoria = input("Categoria (Enter para ignorar): ")
            preco = input("Preco maximo (Enter para ignorar): ")
            tag = input("Tag (Enter para ignorar): ")

            if preco:
                preco = float(preco)
            else:
                preco = None

            cursos = buscar_cursos(
                categoria or None,
                preco,
                tag or None
            )

            encontrou = False

            for curso in cursos:
                encontrou = True
                print("\nTitulo:", curso["titulo"])
                print("Categoria:", curso["categoria"])
                print("Preco:", curso["preco"])
                print("Vagas:", curso["vagas"])

            if not encontrou:
                print("Nenhum curso encontrado!")

        elif opcao == "2":
            matricular_aluno()

        elif opcao == "3":
            atualizar()

        elif opcao == "4":
            avaliar()

        elif opcao == "5":
            exibir_relatorios()

        elif opcao == "0":
            print("Encerrando o programa...")
            break

        else:
            print("Opcao invalida!")


menu()
