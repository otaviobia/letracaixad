#!/bin/bash
echo "=========================================="
echo "🔄  ATUALIZANDO O BLOG (SEM CACHE)..."
echo "=========================================="

# 1. Força a reconstrução do zero (sem aproveitar cache antigo)
# Isso obriga o Astro a bater na API e pegar os posts novos.
docker compose build --no-cache web

# 2. Sobe o novo container
docker compose up -d web

# 3. Limpeza
docker image prune -f

echo "=========================================="
echo "✅  SUCESSO! Site atualizado com dados frescos."
echo "=========================================="
