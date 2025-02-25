# Stage 1: Builder
FROM python:3.12-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Stage 2:
FROM python:3.12-slim-buster

WORKDIR /app

# Copy only the necessary files and directories from the builder stage
COPY --from=builder /app/ /app/
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]