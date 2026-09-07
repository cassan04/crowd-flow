
FROM node:20-alpine AS development

WORKDIR /app

COPY backend/package*.json ./
RUN npm install

COPY backend/ .

EXPOSE 5000

CMD ["npm", "run", "dev"]

FROM node:20-alpine AS production

WORKDIR /app

COPY backend/package*.json ./
RUN npm ci --only=production

COPY backend/ .

EXPOSE 5000

CMD ["node", "index.js"]