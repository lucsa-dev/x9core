#!/usr/bin/env bash
# Verifica se Docker está instalado, rodando e acessível pelo usuário atual.
set -euo pipefail

print_apply_group_help() {
    echo "A sessão atual ainda não aplicou o grupo 'docker'. Opções:"
    echo ""
    if command -v sg &>/dev/null; then
        echo "  Opção A (imediata, sem logout):"
        echo "    sg docker -c \"make up\""
        echo ""
    fi
    echo "  Opção B — logout/login no sistema e rode:"
    echo "    make up"
    echo ""
    if ! command -v newgrp &>/dev/null; then
        echo "  Opção C — instalar newgrp (opcional):"
        echo "    sudo apt install util-linux-extra"
        echo "    newgrp docker"
        echo ""
    else
        echo "  Opção C:"
        echo "    newgrp docker"
        echo ""
    fi
}

if ! command -v docker &>/dev/null; then
    echo "Erro: Docker não encontrado."
    echo ""
    echo "Instale com:"
    echo "  make setup-docker"
    exit 1
fi

if docker info &>/dev/null 2>&1; then
    exit 0
fi

stderr=$(docker info 2>&1 >/dev/null || true)

if echo "$stderr" | grep -qi "permission denied"; then
    echo "Erro: sem permissão para acessar o Docker."
    echo ""
    if groups | grep -qw docker; then
        echo "Você já está no grupo 'docker'."
        print_apply_group_help
    else
        echo "Adicione seu usuário ao grupo docker:"
        echo ""
        echo "  make fix-docker-perms"
        print_apply_group_help
    fi
    exit 1
fi

if echo "$stderr" | grep -qi "cannot connect\|is the docker daemon running"; then
    echo "Erro: Docker daemon não está rodando."
    echo ""
    echo "Inicie com:"
    echo "  sudo systemctl start docker"
    exit 1
fi

echo "Erro ao conectar ao Docker:"
echo "$stderr"
exit 1
