FROM python:3.11-slim
WORKDIR /app

# Dependencias de teste (explicitas e previsiveis)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir pytest pytest-cov
COPY app app
COPY tests tests

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
