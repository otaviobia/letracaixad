# backend/Dockerfile
FROM python:3.12-slim-bookworm

# Instala o gerenciador de pacotes 'uv' (muito mais rápido que o pip)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copia os arquivos de dependência primeiro (para cachear o docker build)
COPY pyproject.toml uv.lock ./

# Instala as dependências do sistema e do projeto
RUN uv sync --frozen --no-install-project

# Copia o resto do código
COPY . .

# Garante que o banco de dados tenha permissão de escrita
# (O SQLite precisa poder criar arquivos de journal na pasta)
RUN chmod -R 777 /app

# Comando para rodar a API
CMD ["uv", "run", "fastapi", "run", "src/main.py", "--port", "8000", "--host", "0.0.0.0"]