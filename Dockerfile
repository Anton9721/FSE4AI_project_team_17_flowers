FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# (не обязательно, но помогает tf cpu)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential python3-dev libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 1) Сначала ставим базовые зависимости (быстрый кеш)
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r requirements.txt

# 2) Затем копируем исходники проекта
COPY model/ model/
COPY app/ app/
COPY .streamlit/ .streamlit/

# 3) И только теперь ставим сам проект (editable)
RUN pip install --no-cache-dir -e .

# (по желанию) включить модель в образ:
# COPY saved_model/ saved_model/

EXPOSE 8501
CMD ["streamlit", "run", "app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
