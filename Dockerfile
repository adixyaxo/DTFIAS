# Stage 1: Build Tailwind CSS
FROM node:20-slim AS frontend-builder
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/app.css --minify

# Stage 2: Build Python Backend
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy built css from the frontend stage
COPY --from=frontend-builder /app/app/static/css/app.css ./app/static/css/app.css

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
