# 📋 TaskCrafter CLI

[![Tests and Coverage](https://i.ytimg.com/vi/jfL6I0VDgGw/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCDIgyqNGN9bFR2zNmXseZOxGqRGw)
[![codecov](https://i.ytimg.com/vi/bNVRxb-MKGo/sddefault.jpg)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Sistema de gerenciamento de tarefas via linha de comando (CLI) desenvolvido em Python para a disciplina de **Teste de Software**.

## 👨‍💻 Autor

**Espezzialy Raphael Oliveira Souza**

## 📖 Sobre o Projeto

TaskCrafter é uma aplicação CLI robusta para gerenciar tarefas com funcionalidades completas de CRUD, filtros avançados, ordenação e persistência em JSON. O projeto demonstra boas práticas de desenvolvimento de software incluindo:

- ✅ Arquitetura modular e orientada a objetos
- ✅ Testes unitários e de integração extensivos (43+ testes)
- ✅ Cobertura de código ≥ 80%
- ✅ CI/CD com GitHub Actions
- ✅ Integração com Codecov para análise de cobertura
- ✅ Validações robustas de dados
- ✅ Documentação completa

## 🚀 Funcionalidades

### Comandos Disponíveis

1. **`add`** - Adicionar nova tarefa
   - Título único (obrigatório)
   - Descrição
   - Prioridade (baixa, media, alta)
   - Tags para categorização
   - Data de vencimento (YYYY-MM-DD)

2. **`list`** - Listar todas as tarefas
   - Filtros: status, prioridade, tag
   - Ordenação: data_criacao, prioridade, titulo, data_vencimento

3. **`update`** - Atualizar tarefa existente
   - Modificar qualquer campo exceto título

4. **`done`** - Marcar tarefa como concluída
   - Define automaticamente data de conclusão

5. **`delete`** - Remover tarefa pelo título

6. **`filter`** - Filtrar tarefas por múltiplos critérios
   - Status, prioridade, tag, data de vencimento
   - Ordenação customizável

7. **`stats`** - Exibir estatísticas das tarefas
   - Total por status
   - Total por prioridade

## 📦 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/USUARIO/taskcrafter.git
cd taskcrafter
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Verifique a instalação:
```bash
python -m taskcrafter --version
```

## 💻 Uso

### Exemplos Básicos

#### Adicionar tarefas
```bash
# Tarefa simples
python -m taskcrafter add "Estudar Python"

# Tarefa completa
python -m taskcrafter add "Fazer compras" -d "Ir ao supermercado" -p alta -t casa urgente -v 2025-11-25
```

#### Listar tarefas
```bash
# Listar todas
python -m taskcrafter list

# Listar com filtro
python -m taskcrafter list -s pendente -p alta

# Ordenar por prioridade
python -m taskcrafter list -o prioridade
```

#### Atualizar tarefa
```bash
python -m taskcrafter update "Estudar Python" -d "Revisar conceitos de OOP" -p alta -s andamento
```

#### Concluir tarefa
```bash
python -m taskcrafter done "Estudar Python"
```

#### Deletar tarefa
```bash
python -m taskcrafter delete "Fazer compras"
```

#### Filtrar tarefas
```bash
# Filtrar por múltiplos critérios
python -m taskcrafter filter -s andamento -p alta -t urgente

# Filtrar por data de vencimento
python -m taskcrafter filter -v 2025-11-25 -o data_vencimento
```

#### Ver estatísticas
```bash
python -m taskcrafter stats
```

### Ajuda

Para ver todos os comandos e opções:
```bash
python -m taskcrafter --help
python -m taskcrafter add --help
```

## 🧪 Testes

O projeto possui uma suite completa de testes com mais de 43 testes unitários e 13 testes de integração/e2e.

### Executar todos os testes
```bash
pytest
```

### Executar com cobertura
```bash
pytest --cov=taskcrafter --cov-report=term-missing
```

### Executar testes específicos
```bash
# Apenas testes unitários
pytest tests/test_models.py
pytest tests/test_manager.py

# Apenas testes de integração
pytest tests/test_integration.py
```

### Gerar relatório HTML de cobertura
```bash
pytest --cov=taskcrafter --cov-report=html
# Abra htmlcov/index.html no navegador
```

### Estrutura de Testes

```
tests/
├── conftest.py           # Fixtures compartilhadas
├── test_models.py        # 18 testes do modelo Task
├── test_manager.py       # 25 testes do TaskManager
└── test_integration.py   # 13 testes de integração/e2e
```

#### Cobertura de Testes

Os testes cobrem:
- ✅ Criação e validação de tarefas
- ✅ Todas as operações CRUD
- ✅ Filtros e ordenação
- ✅ Persistência em JSON
- ✅ Validações de regras de negócio
- ✅ Casos de erro e exceções
- ✅ Fluxos completos de uso (e2e)
- ✅ Múltiplas instâncias e persistência

## 📊 CI/CD

O projeto utiliza **GitHub Actions** para integração e entrega contínuas.

### Workflow Configurado

- ✅ Execução automática em push e pull requests
- ✅ Testes em múltiplas plataformas: Linux, macOS, Windows
- ✅ Testes em múltiplas versões do Python: 3.10, 3.11, 3.12
- ✅ Geração de relatório de cobertura
- ✅ Upload automático para Codecov
- ✅ Verificação de threshold mínimo de cobertura (80%)

### Configuração do Codecov

1. Crie uma conta em [codecov.io](https://codecov.io)
2. Conecte seu repositório GitHub
3. Adicione o token CODECOV_TOKEN nos secrets do repositório:
   - Vá em Settings → Secrets and variables → Actions
   - Adicione um novo secret chamado `CODECOV_TOKEN`
   - Cole o token fornecido pelo Codecov

### Badges

Para atualizar os badges no README, substitua `USUARIO` pelo seu usuário do GitHub:

```markdown
[![Tests](https://i.ytimg.com/vi/GlqQGLz6hfs/sddefault.jpg)
[![codecov](https://i.ytimg.com/vi/AAl4HmJ3YuM/maxresdefault.jpg)
```

## 📁 Estrutura do Projeto

```
taskcrafter_project/
├── taskcrafter/              # Código-fonte principal
│   ├── __init__.py          # Inicialização do pacote
│   ├── __main__.py          # Ponto de entrada CLI
│   ├── models.py            # Modelo de dados (Task)
│   ├── manager.py           # Gerenciador de tarefas (CRUD)
│   └── cli.py               # Interface CLI com argparse
├── tests/                   # Suite de testes
│   ├── conftest.py          # Fixtures do pytest
│   ├── test_models.py       # Testes do modelo
│   ├── test_manager.py      # Testes do gerenciador
│   └── test_integration.py # Testes de integração
├── data/                    # Diretório de dados (criado automaticamente)
│   └── tasks.json           # Arquivo de persistência
├── .github/
│   └── workflows/
│       └── tests.yml        # Workflow CI/CD
├── pyproject.toml           # Configuração do projeto e pytest
├── requirements.txt         # Dependências
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** - Linguagem de programação
- **argparse** - Parser de argumentos CLI (biblioteca padrão)
- **json** - Persistência de dados (biblioteca padrão)
- **dataclasses** - Modelo de dados (biblioteca padrão)
- **pytest** - Framework de testes
- **pytest-cov** - Plugin de cobertura
- **GitHub Actions** - CI/CD
- **Codecov** - Análise de cobertura

## 📋 Requisitos Acadêmicos Atendidos

### ✅ Funcionalidades
- [x] Sistema CLI completo com argparse
- [x] Operações CRUD (Create, Read, Update, Delete)
- [x] Título único e validações de dados
- [x] Prioridades (baixa, média, alta)
- [x] Status (pendente, andamento, concluída)
- [x] Tags para categorização
- [x] Datas no formato ISO (YYYY-MM-DD)
- [x] Filtros e ordenação avançados
- [x] Persistência em JSON

### ✅ Testes
- [x] Mínimo 30 testes unitários (43 implementados)
- [x] Mínimo 5 testes de integração/e2e (13 implementados)
- [x] Cobertura ≥ 80%
- [x] Uso de fixtures do pytest
- [x] Testes focados e não-complexos
- [x] Nomes descritivos

### ✅ CI/CD
- [x] GitHub Actions configurado
- [x] Testes em Linux, macOS e Windows
- [x] Múltiplas versões do Python (3.10, 3.11, 3.12)
- [x] Upload automático para Codecov
- [x] Verificação de cobertura mínima

### ✅ Documentação
- [x] README completo
- [x] Instruções de instalação
- [x] Exemplos de uso
- [x] Como executar testes
- [x] Badges de CI/CD e cobertura
- [x] Estrutura do projeto documentada

## 🤝 Contribuindo

Este é um projeto acadêmico individual, mas sugestões são bem-vindas!

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é desenvolvido para fins acadêmicos na disciplina de Teste de Software.

## 📧 Contato

**Espezzialy Raphael Oliveira Souza**

Projeto desenvolvido como parte da disciplina de Teste de Software.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
