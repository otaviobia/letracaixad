FROM node:20-alpine
WORKDIR /app

# Instala dependências
COPY package.json package-lock.json ./
RUN npm install

# Copia o código do site
COPY . .

# Pega a variável que veio do docker-compose
ARG PUBLIC_API_URL
ENV PUBLIC_API_URL=$PUBLIC_API_URL

ENV HOST=0.0.0.0
ENV PORT=80
EXPOSE 80

# Roda o comando de build (Gera a pasta dist)
RUN npm run build


CMD ["node", "./dist/server/entry.mjs"]
