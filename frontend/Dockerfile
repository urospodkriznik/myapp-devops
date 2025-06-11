# Step 1: build the app
FROM node:20-alpine AS build

WORKDIR /app

# Set backend URL as build arg and expose to Vite
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Step 2: serve with nginx
FROM nginx:stable-alpine

# Copy built frontend to nginx html dir
COPY --from=build /app/dist /usr/share/nginx/html

# Replace default nginx config with simple one
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]