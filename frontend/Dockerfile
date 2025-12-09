# frontend/Dockerfile
FROM node:22-alpine

WORKDIR /app

# Copy package.json first for caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source files
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Start the server
# --host is CRITICAL: It allows the container to be accessed from your browser
CMD ["npm", "run", "dev", "--", "--host"]
