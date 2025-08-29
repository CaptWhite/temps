FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
RUN npm list
COPY . .
ENV NODE_ENV=production
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]