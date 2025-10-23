# Dockerfile
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# зависимости проекта
COPY pyproject.toml ./
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -e .

# код и (опционально) модель
COPY model/ model/
COPY app/ app/
# Если модель обучена локально, можно включить её в образ (по желанию):
# COPY saved_model/ saved_model/

EXPOSE 8501
CMD ["streamlit", "run", "app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
