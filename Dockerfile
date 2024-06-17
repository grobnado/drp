# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файл весов модели
COPY models/trained_model.pth /app/models/trained_model.pth

# Устанавливаем порт, который будет использоваться приложением
ENV PORT=5000

# Запускаем приложение
CMD ["python", "app.py"]
