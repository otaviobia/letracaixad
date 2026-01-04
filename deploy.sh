#!/bin/bash

echo "=========================================="
echo "🔄  ATUALIZANDO O BLOG..."
echo "=========================================="

# 1. Reconstrói APENAS o container 'web' (Frontend)
# O backend e o banco de dados continuam rodando sem interrupção.
docker compose up -d --build web

# 2. Limpeza de casa (Opcional, mas recomendado)
# Remove a imagem antiga que ficou sobrando para liberar espaço em disco.
# O '-f' força a limpeza sem pedir confirmação.
docker image prune -f

echo "=========================================="
echo "✅  SUCESSO! O site foi atualizado."
echo "=========================================="
