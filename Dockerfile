FROM python:3.9-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY service/ ./service/

# Create a non-root user
RUN useradd -u 1000 appuser && chown -R appuser /app
USER appuser

# Expose port 8000
ENV PORT=8000
EXPOSE 8000

# Run service using Gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--log-level=info", "service:app"]
