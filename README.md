# TaskCrafter CLI

Um gerenciador de tarefas de linha de comando em Python, focado em boas práticas de testes automatizados, cobertura e CI/CD.

Autor: Espezzialy Raphael Oliveira Souza

## Sumário
- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Executar Localmente](#como-executar-localmente)
- [Como Executar os Testes Localmente](#como-executar-os-testes-localmente)
- [Cobertura de Testes](#cobertura-de-testes)
- [CI/CD com GitHub Actions](#cicd-com-github-actions)
- [Publicação de Cobertura no Codecov](#publicação-de-cobertura-no-codecov)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Roadmap de Testes](#roadmap-de-testes)
- [Licença](#licença)

## Visão Geral
O TaskCrafter CLI permite criar, listar, atualizar e concluir tarefas, com suporte a prioridades, tags, datas de vencimento e filtros. O objetivo do projeto é demonstrar como testes (unitários e de integração/e2e), cobertura e pipelines de CI/CD facilitam a manutenção e evolução de um sistema.

Persistência local utilizando arquivo JSON, sem dependências de banco de dados. Interface via linha de comando com subcomandos (ex.: `add`, `list`, `done`, `update`, `delete`, `filter`).

## Funcionalidades
- Criar tarefas com:
  - título (obrigatório e único),
  - descrição opcional,
  - prioridade (`baixa`, `media`, `alta`),
  - tags (lista),
  - data de vencimento opcional (YYYY-MM-DD).
- Listar tarefas com filtros:
  - por status (`pendente`, `andamento`, `concluida`),
  - por prioridade,
  - por tag,
  - por vencimento (até uma data),
  - ordenação por vencimento/prioridade/criação.
- Atualizar tarefa (título, descrição, prioridade, tags, vencimento).
- Mudar status: iniciar (`andamento`) e concluir (`concluida`) — conclui define automaticamente `data_conclusao`.
- Remover tarefa pelo título.
- Exportar lista em CSV opcional (para relatórios).
- Armazenamento em `data/tasks.json`.

Regras de negócio principais:
- Título não pode ser vazio e não pode duplicar uma tarefa existente.
- Ao concluir, define `data_conclusao`.
- Prioridade deve ser um dos valores válidos.
- Datas devem estar no formato válido ISO (YYYY-MM-DD).

## Tecnologias Utilizadas
- Linguagem: Python 3.10+
- CLI: `argparse` (ou `typer`/`click` se desejável)
- Testes: `pytest`
- Cobertura: `coverage.py` (via `pytest-cov`)
- Formatação/Lint: `black`, `ruff` (opcional)
- CI/CD: GitHub Actions (builds em Linux, macOS e Windows)
- Publicação de cobertura: Codecov GitHub Action

## Como Executar Localmente
Pré-requisitos:
- Python 3.10 ou superior
- `pip` e `venv`

Passos:
```bash
# 1) Criar e ativar o ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Instalar dependências
pip install -r requirements.txt

# 3) Executar a aplicação (exemplos)
python -m taskcrafter add --title "Estudar testes" --priority alta --tags estudo,python --due 2025-01-10
python -m taskcrafter list --status pendente --order due
python -m taskcrafter done --title "Estudar testes"
python -m taskcrafter delete --title "Estudar testes"