FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

CMD ["pytest", "test_lab1.py", "--cov=main", "--cov-report=term-missing"]
