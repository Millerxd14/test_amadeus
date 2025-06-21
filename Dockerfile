FROM python:3.10

WORKDIR /app

# Variables de entorno para logs inmediatos y configuración
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=2000 -r requirements.txt

COPY . .

# Crear directorios para archivos estáticos
RUN mkdir -p /app/static/images && chmod 777 /app/static/images
RUN mkdir -p /app/static/videos && chmod 777 /app/static/videos

EXPOSE 5660

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5660", "--reload", "--log-level", "info"]
