.PHONY: help up down build logs shell test test-unit test-e2e test-docker lint format install setup setup-docker setup-local dev-local check-docker fix-docker-perms

# Detecta docker ou podman; compose.sh aplica sg docker quando necessário
ifneq ($(shell command -v docker 2>/dev/null),)
  COMPOSE = bash scripts/compose.sh
else ifneq ($(shell command -v podman 2>/dev/null),)
  COMPOSE = podman compose
else
  COMPOSE = bash scripts/check-docker.sh
endif

API_SERVICE = api

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup-docker   - Instala Docker (Ubuntu)"
	@echo "  make fix-docker-perms - Corrige permissão do Docker"
	@echo "  make setup-local    - Venv Python para dev sem Docker"
	@echo "  make up             - Sobe postgres, redis e api"
	@echo "  make down           - Para containers"
	@echo "  make dev-local      - API local (sem containers)"
	@echo "  make test-docker    - Testes no container"
	@echo "  make test           - Testes locais"
	@echo "  make lint           - Ruff + mypy"

check-docker:
	@bash scripts/check-docker.sh

fix-docker-perms:
	@sudo usermod -aG docker "$$USER"
	@echo ""
	@echo "Usuário adicionado ao grupo docker."
	@echo ""
	@echo "Aplique na sessão atual (escolha uma):"
	@echo ""
	@echo "  sg docker -c \"make up\"          # imediato, sem logout"
	@echo "  logout/login e depois: make up"

setup-docker:
	bash scripts/setup-docker.sh

setup-local:
	bash scripts/setup-local.sh

up:
	cp -n .env.example .env 2>/dev/null || true
	$(COMPOSE) up -d postgres redis $(API_SERVICE)

down: check-docker
	$(COMPOSE) down

build: check-docker
	$(COMPOSE) build

logs: check-docker
	$(COMPOSE) logs -f $(API_SERVICE)

shell: check-docker
	$(COMPOSE) exec $(API_SERVICE) bash

install:
	pip install -e ".[dev]"

dev-local:
	@if [ ! -d .venv ]; then \
		echo "Execute primeiro: make setup-local"; \
		exit 1; \
	fi
	. .venv/bin/activate && \
		uvicorn x9core.api.main:app --host 0.0.0.0 --port 8000 --reload

test: test-unit test-e2e

test-unit:
	pytest tests/unit -v --cov=x9core --cov-report=term-missing --cov-fail-under=100

test-e2e:
	pytest tests/e2e -v -m e2e

test-docker: check-docker
	$(COMPOSE) --profile test run --rm test

test-integration:
	pytest tests/integration -v -m integration

lint:
	ruff check src tests
	ruff format --check src tests
	mypy src

format:
	ruff check --fix src tests
	ruff format src tests
