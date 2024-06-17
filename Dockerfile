# Используем базовый образ Python
FROM python:3-dev

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    python3-distutils \
    && apt-get clean

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . /app
WORKDIR /app

# Открываем порт для приложения
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]