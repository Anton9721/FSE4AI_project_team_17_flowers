FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# зависимости
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir -e .

# код (модель будет примонтирована томом при запуске)
COPY model/ model/
COPY app/ app/
COPY .streamlit/ .streamlit/

EXPOSE 8501
CMD ["streamlit", "run", "app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
