def criar_colecao_cursos(banco):
    if "cursos" not in banco.list_collection_names():
        banco.create_collection(
            "cursos",
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": [
                        "titulo",
                        "categoria",
                        "preco",
                        "vagas",
                        "modulos"
                    ],
                    "properties": {
                        "titulo": {
                            "bsonType": "string"
                        },
                        "categoria": {
                            "bsonType": "string"
                        },
                        "preco": {
                            "bsonType": ["double", "int", "long", "decimal"],
                            "minimum": 0
                        },
                        "vagas": {
                            "bsonType": ["int", "long"],
                            "minimum": 0
                        },
                        "modulos": {
                            "bsonType": "array"
                        }
                    }
                }
            }
        )