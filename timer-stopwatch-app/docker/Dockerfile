FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY static/ ./static/
COPY templates/ ./templates/

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "src/app.py"]