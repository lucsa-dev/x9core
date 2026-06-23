# x9core

API de monitoramento e scraping com Google Dorks — **scraping direto**, sem APIs externas pagas.

## Stack

- Python 3.12 + FastAPI
- Arquitetura Hexagonal (Ports & Adapters)
- Playwright + BeautifulSoup (scraping)
- PostgreSQL + Redis
- Docker Compose

## Roadmap

Ver [ROADMAP.md](ROADMAP.md) para o pipeline completo.

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
│   ├── entities/       # SearchHit
│   ├── ports/          # Clock
│   ├── services/       # DorkBuilder, dedup, url normalizer
│   └── value_objects/  # TimeWindow, Dork
├── application/
│   ├── ports/          # SearchProvider
│   └── use_cases/      # SearchByDork
├── infrastructure/
│   └── scraping/       # parser HTML, fakes (Playwright no Step 4)
└── api/                # FastAPI
```

## Padrões de código

- **Docstrings obrigatórias** em classes, funções e métodos em `src/` (validado pelo Ruff)
- Regra detalhada em `.cursor/rules/docstrings.mdc`
- Testes offline com HTML fixtures em `tests/fixtures/`
