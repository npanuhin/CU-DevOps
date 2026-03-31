FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /app/deps /app/deps
COPY main.py .

ENV PYTHONPATH=/app/deps
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]