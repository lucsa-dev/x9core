#!/usr/bin/env bash
# Wrapper do docker compose — usa 'sg docker' se a sessão ainda não tiver o grupo aplicado.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

run_compose() {
    docker compose "$@"
}

if docker info &>/dev/null 2>&1; then
    run_compose "$@"
    exit 0
fi

stderr=$(docker info 2>&1 >/dev/null || true)

if echo "$stderr" | grep -qi "permission denied" && groups | grep -qw docker; then
    if command -v sg &>/dev/null; then
        quoted=$(printf '%q ' "$@")
        exec sg docker -c "cd $(printf '%q' "$ROOT") && docker compose ${quoted}"
    fi
fi

bash "$ROOT/scripts/check-docker.sh"
exit 1
