FROM node:8-alpine as builder

COPY ./rts-front/package.json ./rts-front/package-lock.json ./

RUN npm set progress=false && npm config set depth 0 && npm cache clean --force

RUN npm i && mkdir /ng-app && cp -R ./node_modules ./ng-app

WORKDIR /ng-app

COPY ./rts-front .

RUN $(npm bin)/ng build --prod --build-optimizer

FROM nginx:1.13.3-alpine

## Copy our default nginx config
COPY ./rts-front/default.conf /etc/nginx/conf.d/

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

## From 'builder' stage copy over the artifacts in dist folder to default nginx public folder
COPY --from=builder /ng-app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]