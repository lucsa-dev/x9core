#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip
pip install -e ".[dev]"

echo ""
echo "Ambiente local pronto. Comandos:"
echo "  source .venv/bin/activate"
echo "  make dev-local    # API sem Docker"
echo "  make test         # testes"
