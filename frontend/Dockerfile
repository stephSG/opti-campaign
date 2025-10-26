# Stage 1: Base Node Image for Development
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
# This is done first to leverage Docker cache
COPY package.json ./
RUN npm install

# Copy the rest of the application source code
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Command to run the development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
