#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}==>${NC} $*"; }
warn()  { echo -e "${YELLOW}==>${NC} $*"; }
error() { echo -e "${RED}==>${NC} $*" >&2; }

ensure_docker_group() {
    if groups | grep -qw docker; then
        info "Usuário já está no grupo docker."
        return
    fi
    warn "Adicionando ${USER} ao grupo docker..."
    sudo usermod -aG docker "${USER}"
    warn "Execute 'newgrp docker' ou faça logout/login antes de 'make up'."
}

if command -v docker &>/dev/null; then
    info "Docker já instalado: $(docker --version)"
    if docker compose version &>/dev/null; then
        info "Docker Compose: $(docker compose version --short)"
    fi
    ensure_docker_group
    if docker info &>/dev/null 2>&1; then
        info "Docker acessível. Pronto para 'make up'."
    else
        warn "Docker instalado, mas sem acesso ainda."
        warn "Rode: sg docker -c \"make up\"   (ou logout/login)"
    fi
    exit 0
fi

warn "Docker não encontrado. Instalando..."

if ! command -v sudo &>/dev/null; then
    error "sudo não disponível. Instale manualmente:"
    echo "  sudo apt update"
    echo "  sudo apt install -y docker.io docker-compose-v2"
    echo "  sudo usermod -aG docker \$USER"
    echo "  newgrp docker"
    exit 1
fi

sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2

sudo systemctl enable --now docker
sudo usermod -aG docker "${USER}"

    warn "IMPORTANTE: aplique o grupo docker com uma das opções:"
    warn "  sg docker -c \"make up\"     # imediato"
    warn "  logout/login                 # permanente"
