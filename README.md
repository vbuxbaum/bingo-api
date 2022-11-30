![Pytest](https://github.com/vbuxbaum/bingo-api/actions/workflows/lint-testing-action.yml/badge.svg)
![Deploy](https://github.com/vbuxbaum/bingo-api/actions/workflows/python-app.yml/badge.svg)

# bingo-api
Uma API em Python (FastAPI) para gerar números de uma cartela de Bingo

O [deploy oficial](http://bingo-api.com.br) foi feito no Heroku, onde pode ser acessada a [documentação](http://bingo-api.com.br/docs) dos endpoints.

## Como executar

:eyes: Como é um projeto Python com várias dependências, a boa prática é usar um [ambiente virtual](https://docs.python.org/3/library/venv.html)

Instale as dependências
```bash
pip install -r dev-requirements.txt
```

Execute o comando 

```bash
uvicorn app.main:app --reload
```

> De forma alternativa ao comando anterior, você pode definir as variáveis de ambiente `PORT=8000` e `DEBUG=--reload` e utilizar o comando `heroku local`

### Configurações de ambiente de teste

É necessário definir a variável de ambiente `MONGODB_URL` no arquivo `.env` com a URL para conexão com o banco de dados

Opcionalmente, você pode definir uma variável `API_TOKEN` para os endpoints https://hackmd.io/9Qw7MoHwQZS36prck_5dag#de PUT, POST e DELETE. Localmente, o valor padrão é `""`. No ambiente de produção, há um token previamente definido.


## Tipos de cartelas

### Clássica (`classic`)

É o tipo de cartela mais comum: 5x5, com a casa central vazia.

Os valores (1 até 75) são divididos em 5 intervalos de 15

### Quadrado N x N (`n_square`)

Uma cartela simétrica de tamanho `N`. Se `N` for impar, a casa central ficará vazia.

Os valores (1 até `N^2 * 3`) são divididos em `N` intervalos.

### Quadrado N x N com diagonal vazia (`n_square_diag`)

Uma cartela simétrica de tamanho `N`, com as casas da diagonal (_topo-esquerda > base-direita_) vazias.

Os valores são gerados conforme a regra anterior

## Rounds 

Rounds são "partidas" de bingo, que possuem um tipo de cartela definido, um conjunto de cartelas participantes, e os números já sorteados

## Contribuições

Abra um PR (via fork)! ❤️

Fez um front-end para as renderizar as cartelas? Fala comigo [aqui](https://www.linkedin.com/in/vitorbuxbaum/)!
