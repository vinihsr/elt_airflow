# Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies 
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to a local folder
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Runner
FROM python:3.11-slim AS runner

WORKDIR /app

# Install ONLY the runtime library for PostgreSQL (no gcc or dev tools needed here)
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

# Copy only the installed packages from the builder stage
COPY --from=builder /root/.local /root/.local
# Copy application code
COPY . .

# Ensure the locally installed pip packages are in the PATH
ENV PATH=/root/.local/bin:$PATH

# Final command to execute the pipeline
CMD ["python", "main.py"]