FROM node:20-alpine AS build
WORKDIR /app

COPY package.json next.config.mjs ./
RUN npm install

COPY app ./app
COPY lib ./lib
COPY data ./data
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/out/ /usr/share/nginx/html/
EXPOSE 80
