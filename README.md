# x9core

API de monitoramento e scraping com Google Dorks.

## Stack

- Python 3.12 + FastAPI
- Arquitetura Hexagonal (Ports & Adapters)
- PostgreSQL + Redis
- Docker Compose

## Início rápido

### Com Docker (recomendado)

```bash
# 1. Instalar Docker (se ainda não tiver)
make setup-docker
make fix-docker-perms   # se der "permission denied"

# 2. Subir o projeto
cp .env.example .env
make up               # usa sg docker automaticamente se necessário
make test-docker
```

API disponível em http://localhost:8000/health

### Sem Docker (dev local)

```bash
make setup-local
source .venv/bin/activate
make dev-local
make test
```

## Comandos

| Comando | Descrição |
|---------|-----------|
| `make setup-docker` | Instala Docker no Ubuntu |
| `make setup-local` | Cria venv Python local |
| `make up` | Sobe postgres, redis e api |
| `make dev-local` | API local sem containers |
| `make down` | Para todos os containers |
| `make test` | Testes locais (requer venv) |
| `make test-docker` | Testes dentro do container |
| `make lint` | Ruff + mypy |
| `make logs` | Logs da API |

## Estrutura

```text
src/x9core/
├── domain/
│   ├── ports/          # Interfaces (Clock)
│   ├── services/       # DorkBuilder
│   └── value_objects/  # TimeWindow, Dork
├── application/    # Use cases e ports
├── infrastructure/ # Adapters (SERP, DB, fila)
└── api/            # FastAPI (camada fina)
```

## Padrões de código

- **Docstrings obrigatórias** em classes, funções e métodos em `src/` (validado pelo Ruff)
- Regra detalhada em `.cursor/rules/docstrings.mdc`
