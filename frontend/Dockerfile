# frontend/Dockerfile
FROM nginx:alpine

# Copia a configuração customizada do Nginx (vamos criar abaixo)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos estáticos gerados pelo Astro (pasta dist)
COPY dist /usr/share/nginx/html

EXPOSE 80