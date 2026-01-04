# ESTÁGIO 1: A "FÁBRICA" (Build)
# Usamos uma imagem que já tem Node instalado
FROM node:20-alpine AS builder
WORKDIR /app

# Instala dependências
COPY package.json package-lock.json ./
RUN npm ci

# Copia o código do site
COPY . .

# Pega a variável que veio do docker-compose
ARG PUBLIC_API_URL
ENV PUBLIC_API_URL=$PUBLIC_API_URL

# Roda o comando de build (Gera a pasta dist)
RUN npm run build


# ESTÁGIO 2: A "ENTREGA" (Nginx)
FROM nginx:alpine

# Configurações do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# A MÁGICA: Copia a pasta 'dist' DO estágio anterior (builder)
# Assim não precisamos ter a pasta dist no servidor Ubuntu!
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
