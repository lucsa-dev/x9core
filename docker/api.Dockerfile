FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- deps ---
FROM base AS deps

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --upgrade pip && \
    pip install ".[dev]"

# --- runtime ---
FROM deps AS runtime

EXPOSE 8000

CMD ["uvicorn", "x9core.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- test ---
FROM deps AS test

CMD ["pytest", "tests/unit", "tests/e2e", "-v", "--cov=x9core", "--cov-report=term-missing", "--cov-fail-under=100"]
