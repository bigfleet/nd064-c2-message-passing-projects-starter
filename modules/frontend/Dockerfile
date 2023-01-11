FROM node:lts-alpine as build

WORKDIR /srv

COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

COPY . ./

RUN npm run build --omit=dev

FROM nginx:alpine
COPY --from=build /srv/build/ /usr/share/nginx/html
