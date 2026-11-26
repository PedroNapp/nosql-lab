# Aprenda+ - Catálogo de Cursos MongoDB

Projeto desenvolvido para a atividade de Banco de Dados NoSQL, utilizando Python, PyMongo e MongoDB Atlas.

## 1. Como executar

### Requisitos

- Python instalado.
- Biblioteca PyMongo.
- Acesso ao MongoDB Atlas.

Instale a biblioteca:

```bash
pip install pymongo
```

### Configurar a conexão

### Configurar a conexão

O projeto utiliza o MongoDB Atlas como banco de dados.

No PowerShell, configure as variáveis de conexão:

```powershell
$env:MONGO_USERNAME="<SEU_USUARIO>"
$env:MONGO_PASSWORD="<SUA_SENHA>"
$env:MONGO_URI="mongodb+srv://$($env:MONGO_USERNAME):$($env:MONGO_PASSWORD)@<SEU_CLUSTER>.mongodb.net/?retryWrites=true&w=majority"
$env:MONGO_DB="aprendamais"
```

Substitua os campos entre `< >` pelos dados de acesso e pelo endereço do seu cluster MongoDB Atlas.

A conexão é realizada pelo arquivo `mongo_cursos/conexao.py`, utilizando as variáveis `MONGO_URI` e `MONGO_DB`.

### Executar a carga inicial

Na pasta principal do projeto, execute:

```bash
python -m mongo_cursos.seed
```

A carga inicial insere:

- 30 cursos distribuídos em 5 categorias;
- 10 alunos;
- 30 matrículas.

O script utiliza `insert_many()` e `random` para gerar os dados. Também verifica se já existem registros para evitar duplicações.

### Executar o sistema

```bash
python -m mongo_cursos.main
```

## 2. Justificativa da modelagem dos dados

O banco utiliza três coleções: `cursos`, `alunos` e `matriculas`. A organização foi definida considerando a relação entre os dados, a forma como serão consultados e o limite de 16 MB por documento do MongoDB.

**Cursos - Embedding (dados embutidos)**

O instrutor e os módulos ficam dentro do próprio documento do curso. Escolhemos essa estrutura porque essas informações pertencem ao curso e normalmente são necessárias quando sua página é consultada.

Assim, ao buscar um curso, já temos acesso ao instrutor e aos módulos na mesma consulta, sem precisar procurar esses dados em outras coleções.

Essa escolha também é adequada porque a quantidade de módulos pertence à estrutura do curso e não aumenta a cada nova matrícula de aluno.

**Alunos - Documentos separados**

Os alunos possuem uma coleção própria porque são entidades independentes. Um mesmo aluno pode estar matriculado em vários cursos, portanto seus dados não precisam ser repetidos dentro de cada curso ou matrícula.

Dessa forma, podemos consultar e atualizar os dados de um aluno separadamente.

**Matrículas - Linking (referências)**

As matrículas ficam em uma coleção própria e utilizam `aluno_id` e `curso_id` para identificar o aluno e o curso relacionados.

Escolhemos essa estrutura porque um curso pode ter muitos alunos e um aluno pode participar de vários cursos. Além disso, cada matrícula possui informações próprias, como data, progresso e nota, que podem ser consultadas e atualizadas individualmente.

Se todas as matrículas fossem embutidas no documento do curso, ele cresceria conforme novos alunos fossem matriculados, podendo ultrapassar o limite de 16 MB do MongoDB.

Por isso, manter as matrículas separadas facilita seu gerenciamento e evita o crescimento excessivo dos documentos dos cursos.

## 3. Validação dos dados

A coleção `cursos` possui validação utilizando `$jsonSchema`, exigindo os seguintes campos e regras:

- `titulo`: obrigatório.
- `categoria`: obrigatório.
- `preco`: maior ou igual a zero.
- `vagas`: maior ou igual a zero.
- `modulos`: deve ser um array.

### Demonstração de preço negativo

O arquivo `teste_validacao.py` realiza uma tentativa de inserir um curso com preço negativo:

```python
import pymongo
from mongo_cursos.conexao import obter_banco

banco = obter_banco()

try:
   banco.cursos.insert_one({
      "titulo": "Curso de Teste",
      "categoria": "Programacao",
      "preco": -50.00,
      "vagas": 10,
      "modulos": []
   })

   print("Validador NÃO está ativo!")

except pymongo.errors.WriteError:
   print("Validador ativo! Preço negativo rejeitado.")
```

Execute:

```bash
python teste_validacao.py
```

Resultado esperado:

```text
Validador ativo! Preço negativo rejeitado.
```

O MongoDB rejeita a inserção por causa das regras de validação configuradas na coleção.

## 4. Operações CRUD

As operações estão implementadas no arquivo `repositorio.py`.

- `buscar_cursos()`: pesquisa cursos por categoria, preço máximo e tag, sem retornar os módulos.
- `adicionar_modulo()`: utiliza `$push` para adicionar módulos.
- `atualizar_progresso()`: utiliza `$set` para atualizar o progresso e marcar a matrícula como concluída ao atingir 100%.
- `remover_aluno()`: remove o aluno e suas respectivas matrículas.

## 5. Menu principal

O arquivo `main.py` apresenta um menu de terminal com as seguintes opções:

1. Buscar cursos.
2. Matricular aluno.
3. Atualizar progresso.
4. Avaliar curso.
5. Exibir os três relatórios.
0. Sair.

O sistema verifica a existência do aluno e do curso, impede matrículas duplicadas e não permite matrículas em cursos sem vagas.

As avaliações são permitidas somente após a conclusão do curso, com notas de 1 a 5.

Os três relatórios apresentam cursos e vagas, quantidade de matrículas por curso e desempenho dos alunos.

## 6. Pergunta da atividade

**Em que situação embutir as matrículas dentro do documento do curso seria um erro de modelagem?**

Seria um erro quando um curso possui muitos alunos matriculados, fazendo com que o documento cresça continuamente e possa atingir o limite de 16 MB do MongoDB. Além disso, as matrículas possuem informações próprias, como progresso e nota, que precisam ser consultadas e atualizadas individualmente. Nesse caso, é mais adequado manter as matrículas em uma coleção separada, utilizando referências para alunos e cursos. Dependendo da quantidade de relacionamentos e da necessidade de integridade entre os dados, um banco de dados relacional também pode ser uma escolha mais adequada.