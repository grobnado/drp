
FROM python:3.9-slim

# Устанавливаю зависимости системы
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && apt-get clean

# Устанавливаю зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирую исходный код приложения в контейнер
COPY . /app
WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]
