# First stage: Python build stage
FROM python:3.11-slim-buster AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc

# Copy over and install the poetry dependency files
COPY ./pyproject.toml ./poetry.lock /app/

# Install poetry and dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install poetry==1.5.1 \
    && poetry config virtualenvs.create false \
    && poetry install --only main

# Second stage: development stage
FROM python:3.11-slim-buster AS develop

WORKDIR /app

# Copy from builder stage the installed dependencies
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the source code of the application
COPY . /app/

CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "8080"]
