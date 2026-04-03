FROM python:3.11-slim AS build
WORKDIR /app

RUN pip install --no-cache-dir mkdocs==1.6.1

COPY mkdocs.yml ./
COPY data ./data
COPY scripts ./scripts
RUN python3 scripts/generate_docs.py
RUN mkdocs build

FROM nginx:1.27-alpine
COPY --from=build /app/site/ /usr/share/nginx/html/
EXPOSE 80
