FROM node:20-slim

WORKDIR /app

COPY package.json package-lock.json ./

COPY . .
RUN npm ci

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "--port", "3000"]
