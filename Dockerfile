FROM python:3.10

# рабочую директорию в /app
WORKDIR /app

# Скопируем зависимости приложения в контейнер
COPY requirements.txt .

# Установим зависимости
RUN pip install --upgrade pip
RUN pip install pymysql
RUN pip install -r requirements.txt

# Скопируем все содержимое текущей директории в контейнер в /app
COPY . .

# Запуск
CMD ["python", "app.py"]
