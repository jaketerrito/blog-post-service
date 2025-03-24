# Base stage for shared dependencies
FROM python:3.13-slim-bookworm AS base
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM base AS development
COPY requirements-dev.txt .
RUN pip install --no-cache-dir --upgrade -r requirements-dev.txt

# Production stage - clean image without dev dependencies
FROM base AS server
# Copy application code
COPY . .
# Production command without --reload for better performance
CMD ["fastapi", "run", "src/main.py"]
