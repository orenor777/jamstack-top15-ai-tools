# Reproducible container wrapper for the Pelican static variant.
# The current batch commits built static output in dist/ so this Dockerfile can
# validate and serve the exact artifact deterministically. A later native
# framework implementation can replace the validation step with the framework's
# build command while keeping the same container entrypoint pattern.

FROM python:3.11-slim AS validate
WORKDIR /workspace
COPY dist/ ./dist/
RUN test -f dist/index.html
RUN test -f dist/styles.css

FROM nginx:1.27-alpine
COPY --from=validate /workspace/dist/ /usr/share/nginx/html/
EXPOSE 80
