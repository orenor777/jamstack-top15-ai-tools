FROM alpine:3.20 AS build
WORKDIR /app

RUN apk add --no-cache hugo python3

COPY config.toml ./
COPY data ./data
COPY layouts ./layouts
COPY static ./static
COPY scripts ./scripts
RUN python3 scripts/generate_content.py
RUN hugo --minify

FROM nginx:1.27-alpine
COPY --from=build /app/public/ /usr/share/nginx/html/
EXPOSE 80
