FROM python:3.10-slim

WORKDIR /app

# Копіюємо та встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Відкриваємо порт
EXPOSE 5000

# Запуск через gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]