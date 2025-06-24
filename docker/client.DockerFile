# Build stage
FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY ./client/package*.json ./

# Install dependencies with legacy-peer-deps flag to bypass React version conflicts
RUN npm ci --legacy-peer-deps

# Copy client source code
COPY ./client ./

# Build the React app
RUN npm run build || true

# Production stage with Nginx
FROM nginx:stable-alpine

# Copy the built app to nginx's serve directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY ./client/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Command to run Nginx
CMD ["nginx", "-g", "daemon off;"]