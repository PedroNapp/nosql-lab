import pymongo
from mongo_cursos.conexao import obter_banco

banco = obter_banco()

try:
    banco.cursos.insert_one({
        "titulo": "Curso de Teste",
        "categoria": "Programação",
        "preco": -50.00,
        "vagas": 10,
        "modulos": []
    })

    print("Validador NÃO está ativo!")

except pymongo.errors.WriteError:
    print("Validador ativo! Preço negativo rejeitado.")