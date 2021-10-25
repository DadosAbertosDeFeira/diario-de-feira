# Diário de Feira

Um bot para informar a população sobre o que acontece no Diário Oficial. 📰

[![CI](https://github.com/DadosAbertosDeFeira/diario-de-feira/actions/workflows/cicd.yml/badge.svg)](https://github.com/DadosAbertosDeFeira/diario-de-feira/actions/workflows/cicd.yml) [![Agendamento de postagens de tweets](https://github.com/DadosAbertosDeFeira/diario-de-feira/actions/workflows/schedule.yml/badge.svg)](https://github.com/DadosAbertosDeFeira/diario-de-feira/actions/workflows/schedule.yml)

## Visão

A ideia desse projeto é ser um serviço genérico
de acesso a uma fonte de dados (APIs) que disponibilizam informações
sobre a publicação de edições do Diário Oficial de um município e as
publica em outros locais para serem vistos e acessados pela população
(e.g. Twitter, Discord).

## Configurando o ambiente

- Alguns pré-requisitos necessários:
    - Ter o [Python](https://www.python.org/downloads/) instalado na sua máquina, aqui estamos usando a versão 3.9.5.
    - Ter também, o [Poetry](https://python-poetry.org/docs/master/#installation) instalado na sua máquina. É com ele que vamos gerenciar todas as nossas dependências e criar nosso ambiente virtual.
- Após a instalação do Poetry, vamos instalar as dependências usando:

```
poetry install
```

- Depois iremos iniciar o ambiente virtual usando o shell do poetry:

```
poetry shell
```

Execute também o `pre-commit install` e `pre-commit` para garantir que o seu código esteja formatado
de acordo com o estilo do projeto a cada commit novo.

## Configurando variáveis de ambiente

As variáveis de ambiente deverão ser incluídas em um arquivo chamado `.env`. Deixamos o arquivo `.env-sample` na raíz do projeto pra ser usado como referência na criação do seu arquivo `.env`. Nele estão todas as variáveis que o projeto necessita.

## Rodando o projeto

Dentro do seu ambiente virtual, basta rodar:
```
diario_bot
```

## Executando os testes

Para rodar os testes basta executar:

```
pytest
```
