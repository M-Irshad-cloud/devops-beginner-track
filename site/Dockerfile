FROM nginx:alpine
ARG VERSION=v1
COPY site.conf /etc/nginx/conf.d/default.conf
COPY public/ /usr/share/nginx/html/
RUN sed -i "s/__VERSION__/${VERSION}/g" /usr/share/nginx/html/index.html
