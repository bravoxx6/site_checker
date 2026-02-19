FROM python:3.10-slim

# Устанавливаем единую рабочую директорию
WORKDIR /first_project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое папки FIRST_PROJECT в /app
COPY . .

# По умолчанию запускаем мониторинг
CMD ["python", "app/main.py"]