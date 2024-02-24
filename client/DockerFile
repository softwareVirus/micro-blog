FROM node:19

WORKDIR /app

ADD package.json package-lock.json ./

RUN npm install

RUN npm i vuex@3

ADD babel.config.js vue.config.js ./

CMD [ "npm", "run", "serve" ]