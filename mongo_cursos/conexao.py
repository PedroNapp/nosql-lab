import pymongo
import os

def obter_banco():
    uri = os.getenv("MONGO_URI")
    nome_banco = os.getenv("MONGO_DB")

    cliente = pymongo.MongoClient(uri)

    banco = cliente[nome_banco]

    return banco