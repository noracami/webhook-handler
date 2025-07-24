# Multi-stage Dockerfile for Statuspage to Discord Webhook Service
# Stage 1: Dependencies installation
FROM python:3.12-slim as dependencies

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies to virtual environment
RUN uv sync --frozen --no-dev

# Stage 2: Runtime image
FROM python:3.12-slim as runtime

# Create non-root user for security
RUN groupadd -g 1001 app && \
    useradd -r -u 1001 -g app app

# Set working directory
WORKDIR /app

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy application source code
COPY src/ ./src/
COPY main.py ./

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check using the built-in health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=5.0)"

# Set entrypoint
ENTRYPOINT ["python", "main.py"]