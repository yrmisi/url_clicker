FROM nginx:1.29-alpine

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY frontend/static /app/static

COPY docker_build/frontend/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
