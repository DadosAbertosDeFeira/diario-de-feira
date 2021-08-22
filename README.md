# Diário de Feira

Um bot para informar a população sobre o que acontece no Diário Oficial. 📰

[![CI](https://github.com/DadosAbertosDeFeira/diario-de-feira/actions/workflows/cicd.yml/badge.svg)](https://github.com/DadosAbertosDeFeira/diario-de-feira/actions/workflows/cicd.yml)

## Visão

A ideia desse projeto é ser um serviço genérico
de acesso a uma fonte de dados (APIs) que disponibilizam informações
sobre a publicação de edições do Diário Oficial de um município e as
publica em outros locais para serem vistos e acessados pela população
(e.g. Twitter, Discord).

## Pré-requisitos

- Ter o [Python](https://www.python.org/downloads/) instalado na sua máquina, aqui estamos usando a versão 3.9.5.
- Com o python instalado, é preferível que você tenha um [ambiente virtual](https://docs.python.org/pt-br/3/tutorial/venv.html) para o projeto. Para criar, use os comandos:

```
python3 -m venv venv  # Cria o ambiente virtual
source venv/bin/activate  # Ativa
pip install --upgrade pip  # Upgrade pip
```

Feito isso, estamos prontos para a instalação das dependências.

## Dependências

Para a instalação das dependências, com seu ambiente virtual ativado, use o comando:

```
pip install -r requirements.txt
```

Execute também o `pre-commit install` e `pre-commit` para garantir que o seu código esteja formatado
de acordo com o estilo do projeto a cada commit novo.

## Executando os testes

Para rodar os testes basta executar:

```
pytest
```
