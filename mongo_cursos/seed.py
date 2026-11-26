
import random

from mongo_cursos.conexao import obter_banco
from mongo_cursos.validacao import criar_colecao_cursos


def carregar_dados():
    banco = obter_banco()

    criar_colecao_cursos(banco)

    banco.alunos.create_index("email", unique=True)

    banco.matriculas.create_index(
        [("aluno_id", 1), ("curso_id", 1)],
        unique=True
    )

    if banco.cursos.find_one() or banco.alunos.find_one() or banco.matriculas.find_one():
        print("Os dados ja foram cadastrados!")
        return

    temas = {
        "Programacao": [
            "Python", "JavaScript", "Java", "C#",
            "HTML e CSS", "Git e GitHub", "Desenvolvimento Web",
            "Logica de Programacao", "APIs", "Programacao Orientada a Objetos"
        ],
        "Dados": [
            "Analise de Dados", "SQL", "Power BI", "Excel",
            "Python para Dados", "Visualizacao de Dados",
            "Banco de Dados", "Estatistica", "Dashboards", "Planilhas"
        ],
        "Design": [
            "UI Design", "UX Design", "Figma", "Tipografia",
            "Design Grafico", "Prototipacao", "Identidade Visual",
            "Composicao Visual", "Design de Interfaces", "Ilustracao Digital"
        ],
        "Marketing": [
            "Marketing Digital", "Redes Sociais", "SEO",
            "Marketing de Conteudo", "Email Marketing", "Trafego Pago",
            "Branding", "Copywriting", "Campanhas", "Metricas"
        ],
        "Tecnologia": [
            "Computacao em Nuvem", "Seguranca da Informacao",
            "Redes de Computadores", "Internet das Coisas",
            "Infraestrutura de TI", "Sistemas Operacionais",
            "Suporte Tecnico", "Virtualizacao", "Hardware", "Tecnologia Web"
        ]
    }

    modelos_titulo = [
        "Fundamentos de {}",
        "Introducao a {}",
        "{} na Pratica",
        "Projetos com {}",
        "Conceitos de {}"
    ]

    instrutores = [
        {"nome": "Ana Lima", "email": "ana@email.com"},
        {"nome": "Carlos Souza", "email": "carlos@email.com"},
        {"nome": "Mariana Costa", "email": "mariana@email.com"},
        {"nome": "Rafael Oliveira", "email": "rafael@email.com"},
        {"nome": "Juliana Martins", "email": "juliana@email.com"},
        {"nome": "Pedro Henrique", "email": "pedro@email.com"},
        {"nome": "Fernanda Alves", "email": "fernanda@email.com"},
        {"nome": "Lucas Santos", "email": "lucas@email.com"}
    ]

    tags_disponiveis = [
        "iniciante", "intermediario", "avancado",
        "pratica", "teoria", "online", "projeto",
        "web", "dados", "certificado", "gratuito"
    ]

    titulos_modulos = [
        "Introducao",
        "Fundamentos",
        "Conceitos principais",
        "Ferramentas",
        "Aplicacao pratica",
        "Exercicios",
        "Estudos de caso",
        "Projeto final",
        "Boas praticas",
        "Conclusao"
    ]

    aulas_disponiveis = [
        "Introducao ao assunto",
        "Conceitos basicos",
        "Principais ferramentas",
        "Exercicios praticos",
        "Estudo de caso",
        "Atividade pratica",
        "Revisao do conteudo",
        "Desenvolvimento de projeto",
        "Exemplos de aplicacao",
        "Conclusao do modulo"
    ]

    cursos = []

    for categoria in temas:
        temas_escolhidos = random.sample(temas[categoria], 6)

        for tema in temas_escolhidos:
            titulo = random.choice(modelos_titulo).format(tema)

            quantidade_modulos = random.randint(3, 8)

            modulos = []

            modulos_escolhidos = random.sample(
                titulos_modulos, quantidade_modulos
            )

            for i in range(quantidade_modulos):
                modulo = {
                    "ordem": i + 1,
                    "titulo": modulos_escolhidos[i],
                    "aulas": random.sample(
                        aulas_disponiveis,
                        random.randint(2, 4)
                    )
                }

                modulos.append(modulo)

            curso = {
                "titulo": titulo,
                "categoria": categoria,
                "carga_horaria": random.choice([20, 30, 40, 60, 80, 100]),
                "preco": round(random.uniform(79.90, 599.90), 2),
                "vagas": random.randint(20, 50),
                "tags": random.sample(
                    tags_disponiveis,
                    random.randint(2, 5)
                ),
                "instrutor": random.choice(instrutores),
                "modulos": modulos
            }

            cursos.append(curso)

    resultado_cursos = banco.cursos.insert_many(cursos)

    nomes = [
        "Ana", "Bruno", "Camila", "Daniel", "Eduarda",
        "Felipe", "Gabriela", "Henrique", "Isabela", "Joao",
        "Larissa", "Marcos", "Natalia", "Otavio", "Paula",
        "Rafael", "Sofia", "Thiago", "Vanessa", "Lucas"
    ]

    sobrenomes = [
        "Silva", "Santos", "Oliveira", "Souza", "Costa",
        "Lima", "Pereira", "Ferreira", "Alves", "Rocha",
        "Martins", "Carvalho", "Ribeiro", "Mendes", "Nunes"
    ]

    nomes_completos = []

    for nome in nomes:
        for sobrenome in sobrenomes:
            nomes_completos.append(nome + " " + sobrenome)

    alunos = []

    for nome in random.sample(nomes_completos, 10):
        aluno = {
            "nome": nome,
            "email": nome.lower().replace(" ", ".") + "@aprendamais.com",
            "data_cadastro": random.choice([
                "2026-08-10",
                "2026-09-15",
                "2026-10-02",
                "2026-10-20",
                "2026-11-05"
            ])
        }

        alunos.append(aluno)

    resultado_alunos = banco.alunos.insert_many(alunos)

    matriculas = []

    vagas_iniciais = {}
    matriculas_por_curso = {}

    for curso, curso_id in zip(cursos, resultado_cursos.inserted_ids):
        vagas_iniciais[curso_id] = curso["vagas"]
        matriculas_por_curso[curso_id] = 0

    datas_matricula = [
        "2026-11-10",
        "2026-11-12",
        "2026-11-15",
        "2026-11-18",
        "2026-11-20",
        "2026-11-22",
        "2026-11-23"
    ]

    for aluno_id in resultado_alunos.inserted_ids:
        cursos_escolhidos = random.sample(
            resultado_cursos.inserted_ids, 3
        )

        for curso_id in cursos_escolhidos:
            progresso = random.choice([0, 10, 25, 40, 50, 75, 90, 100])

            matricula = {
                "aluno_id": aluno_id,
                "curso_id": curso_id,
                "data_matricula": random.choice(datas_matricula),
                "progresso": progresso,
                "concluida": progresso == 100,
                "nota": random.randint(1, 5) if progresso == 100 else None
            }

            matriculas.append(matricula)

            matriculas_por_curso[curso_id] += 1

    banco.matriculas.insert_many(matriculas)

    for curso_id in resultado_cursos.inserted_ids:
        vagas_restantes = (
            vagas_iniciais[curso_id] - matriculas_por_curso[curso_id]
        )

        banco.cursos.update_one(
            {"_id": curso_id},
            {"$set": {"vagas": vagas_restantes}}
        )

    print("Carga inicial realizada com sucesso!")
    print("Cursos:", len(cursos))
    print("Alunos:", len(alunos))
    print("Matriculas:", len(matriculas))


carregar_dados()