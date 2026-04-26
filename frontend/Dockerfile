# -- Etape 1 : Build de l'application Vue.js --
FROM node:20-alpine AS build-stage
WORKDIR /app
# On copie les dépendances et on installe
COPY package*.json ./
RUN npm install
# On copie le reste du code de ton binôme et on compile
COPY . .
RUN npm run build 

# -- Etape 2 : Serveur Nginx --
FROM nginx:alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]