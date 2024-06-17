# Используем более легкий базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем зависимости по одному, чтобы избежать проблем с ресурсами
RUN pip install --no-cache-dir Flask \
    && pip install --no-cache-dir flask-cors \
    && pip install --no-cache-dir torch \
    && pip install --no-cache-dir librosa \
    && pip install --no-cache-dir pandas \
    && pip install --no-cache-dir numpy \
    && pip install --no-cache-dir scikit-learn \
    && pip install --no-cache-dir torchvision \
    && pip install --no-cache-dir gunicorn 
# Копируем оставшиеся файлы приложения в контейнер
COPY . /app

# Устанавливаем порт, который будет использоваться приложением
ENV PORT=80

# Запускаем приложение
CMD ["python", "app.py"]
