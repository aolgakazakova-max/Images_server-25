FROM python:3.12-slim

WORKDIR /app

# копируем зависимости
COPY requirements.txt .

# устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь проект
COPY . .

EXPOSE 3000

CMD ["python", "app.py"]
